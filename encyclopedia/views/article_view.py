from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models
from encyclopedia.helpers import check_role

# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar um novo artigo (requer que o usuário esteja logado como Admin ou Staff)
@api_view(['POST'])
def create_artigo(request):
    if check_role(request):
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
    else:
        return Response({
            "error": "O usuário não tem permissão para criar artigos."
        }, status=status.HTTP_400_BAD_REQUEST)

# Listar artigos com limite e ordenação
@api_view(['GET'])
def list_articles(request, quantity=20):
    try:
        quantity = int(quantity)
    except ValueError:
        return Response({"error": "Quantidade inválida."}, status=status.HTTP_400_BAD_REQUEST)

    # Ordenar por número de likes (decrescente), depois por data de criação (mais recente primeiro)
    artigos = models.Artigo.objects.all().order_by('-views', '-created_at')[:quantity]
    serializer = serializers.ArtigoSerializer(artigos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Obter artigo por ID
@api_view(['GET'])
def get_article_by_id(request, id):
    try:
        artigo = models.Artigo.objects.get(id=id)
        serializer = serializers.ArtigoSerializer(artigo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except models.Artigo.DoesNotExist:
        return Response({"error": "O Artigo não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    

# Deletar um artigo (requer login e ser Admin ou Staff)
@api_view(['DELETE'])
def delete_artigo(request, article_id):
    if check_role(request):
        artigo = get_object_or_404(models.Artigo, id=article_id)
        artigo.delete()
        return Response({"message": "Artigo deletado com sucesso."}, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": "O usuário não tem permissão para deletar artigos."
        }, status=status.HTTP_400_BAD_REQUEST)

# Atualizar um artigo (requer login e ser Admin ou Staff)
@api_view(['PUT'])
def update_artigo(request, article_id):
    if check_role(request):
        artigo = get_object_or_404(models.Artigo, id=article_id)
        serializer = serializers.ArtigoSerializer(artigo, data=request.data, partial=True)  # partial=True para permitir atualização parcial

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "error": "O usuário não tem permissão para atualizar artigos."
        }, status=status.HTTP_400_BAD_REQUEST)

