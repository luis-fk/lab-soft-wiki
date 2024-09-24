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

#Criar um novo artigo, mas precisa estar logado como Admin ou Staff.
#Listar todos os artigos
#Deletar um artigo
#Atualizar um artigo

# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar um novo artigo (requer que o usuário esteja logado como Admin ou Staff)
@api_view(['POST'])
@login_required(login_url='/login/')  # Redireciona para login se o usuário não estiver logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def create_artigo(request):
    title = request.POST.get('title')
    text = request.POST.get('text')

    if not title or not text:
        messages.error(request, "Title and text are required.")

    if models.Artigo.objects.filter(title=title).exists():
        messages.error(request, "Title already exists.")
        
    models.Artigo.objects.create(title=title, text=text)

# Listar todos os artigos
@api_view(['GET'])
def list_artigo(request):
    artigo = models.Artigo.objects.all()
    serializer = serializers.ArtigoSerializer(artigo, context={'request': request}, many=True)
    return Response(serializer.data)

# Deletar um artigo
@login_required(login_url='/login/')  # Redireciona para login se o usuário não estiver logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
@api_view(['GET'])
def delete_artigo(request):
    artigo = models.Artigo.objects.all()
    serializer = serializers.ArtigoSerializer(artigo, context={'request': request}, many=True)
    return Response(serializer.data)

# Atualizar um artigo
@login_required(login_url='/login/')  # Redireciona para login se o usuário não estiver logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
@api_view(['GET'])
def update_artigo(request):
    artigo = models.Artigo.objects.all()
    serializer = serializers.ArtigoSerializer(artigo, context={'request': request}, many=True)
    return Response(serializer.data)

