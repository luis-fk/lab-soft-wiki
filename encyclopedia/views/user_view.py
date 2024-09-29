from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models

# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar o usuário da wiki
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if models.User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    if models.User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = models.User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Listar todos os usuários da wiki
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Apenas usuários autenticados podem listar usuários
def list_user(request):
    users = models.User.objects.all()
    serializer = serializers.UserSerializer(users, many=True)
    return Response(serializer.data)

# Deletar um usuário da wiki usando o ID do usuário
@api_view(['DELETE'])
@login_required(login_url='/login/')  # Garante que o usuário esteja logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def delete_user(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    user.delete()
    return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

# Atualizar informações de um usuário da wiki usando o ID do usuário
@api_view(['PUT'])
@login_required(login_url='/login/')  # Garante que o usuário esteja logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def update_user(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    serializer = serializers.UserSerializer(user, data=request.data, partial=True)  # partial=True permite atualização parcial

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
