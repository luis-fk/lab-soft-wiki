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

# Deletar um usuário da wiki usando o ID do usuário
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
# Atualizar informações de um usuário da wiki usando o ID do usuário
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=request.data, partial=True)  # Partial=True permite atualizar apenas alguns campos

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)