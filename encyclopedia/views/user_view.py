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
#Criar o usuário da wiki
#Listar o usuário da wiki
#Deletar o usuário da wiki
#Atualizar o usuário da wiki

# Criar o usuário da wiki
@api_view(['POST'])
def create_user(request):
    if request.method != 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email:
            messages.error(request, "Username and email are required.")

        if models.User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        if models.User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")

        models.User.objects.create(
            username=username,
            email=email,
            password=password,
        )

# Listar o usuário da wiki
@api_view(['GET'])
def list_user(request):
    user = models.User.objects.all()
    serializer = serializers.UserSerializer(user, context={'request': request}, many=True)
    return Response(serializer.data)

# Deletar o usuário da wiki
@api_view(['GET'])
def delete_user(request):
    user = models.User.objects.all()
    serializer = serializers.UserSerializer(user, context={'request': request}, many=True)
    return Response(serializer.data)

# Atualizar o usuário da wiki
@api_view(['GET'])
def update_user(request):
    user = models.User.objects.all()
    serializer = serializers.UserSerializer(user, context={'request': request}, many=True)
    return Response(serializer.data)
