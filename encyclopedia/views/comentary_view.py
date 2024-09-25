from django.shortcuts import render
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import random
import os
from . import helpers
from . import util
from . import serializers
from . import models

#SUMÁRIO:
#Criar Comentário
#Listar todos os comentários
#Deletar um comentário
#Atualizar um comentário

# Criar um novo comentário requer login
@login_required(login_url='/login/')  # Redireciona para login se o usuário não estiver logado
@api_view(['POST'])
def create_comentary(request):
    text = request.POST.get('text')
    if not text:
        messages.error(request, "O texto é necessário")        
    models.Comentario.objects.create(text=text)

# Listar todos os artigos
@api_view(['GET'])
def list_comments(request):
    comentarios = models.Artigo.objects.all()
    serializer = serializers.CommentSerializer(comentarios, context={'request': request}, many=True)
    return Response(serializer.data)

# Deletar um comentário (requer login e ser Admin ou Staff) - usa o ID do artigo. 
@login_required(login_url='/login/')  # Garante que o usuário esteja logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
@api_view(['DELETE'])
def delete_comment(request, commentary_id):
    try:
        comentario = models.Comentario.objects.get(id=commentary_id)
    except models.Comentario.DoesNotExist:
        return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    comentario.delete()
    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)


# Atualizar um comentário (requer login e ser Admin ou Staff), além de usar o ID do artigo.
@login_required(login_url='/login/')  # Garante que o usuário esteja logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
@api_view(['PUT'])
def update_artigo(request, artigo_id):
    try:
        comentario = models.Comentario.objects.get(id=artigo_id)
    except models.Comentario.DoesNotExist:
        return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ComentarioSerializer(comentario, data=request.data, partial=True)  # partial=True para permitir atualização parcial

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
