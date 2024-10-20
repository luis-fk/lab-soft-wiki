from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models


# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar um novo artigo (requer que o usuário esteja logado como Admin ou Staff)
@api_view(['POST'])
def create_artigo(request):
    # Extração dos campos necessários
    user_id = request.data.get('user_id')
    title = request.data.get('title')
    text = request.data.get('text')

    # Verificação dos campos obrigatórios
    if not user_id or not title or not text:
        return Response({
            "error": "Os campos 'user_id', 'title' e 'text' são obrigatórios."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Criação do artigo com os dados fornecidos
    artigo = models.Artigo.objects.create(
        user_id=user_id,
        title=title,
        text=text
    )

    # Resposta de sucesso ao front-end
    return Response({
        "message": "Artigo criado com sucesso!",
        "artigo_id": artigo.id
    }, status=status.HTTP_201_CREATED)


# Listar todos os artigos
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_artigo(request):
    artigos = models.Artigo.objects.all()
    serializer = serializers.ArtigoSerializer(artigos, many=True)
    return Response(serializer.data)

# Deletar um artigo (requer login e ser Admin ou Staff)
@api_view(['DELETE'])
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def delete_artigo(request, artigo_id):
    artigo = get_object_or_404(models.Artigo, id=artigo_id)
    artigo.delete()
    return Response({"message": "Artigo deleted successfully."}, status=status.HTTP_200_OK)

# Atualizar um artigo (requer login e ser Admin ou Staff)
@api_view(['PUT'])
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def update_artigo(request, artigo_id):
    artigo = get_object_or_404(models.Artigo, id=artigo_id)
    
    serializer = serializers.ArtigoSerializer(artigo, data=request.data, partial=True)  # partial=True para permitir atualização parcial

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
