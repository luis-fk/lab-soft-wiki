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
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def create_artigo(request):
    serializer = serializers.ArtigoSerializer(data=request.data)
    
    if serializer.is_valid():
        # Set the 'user' field to the currently authenticated user
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
