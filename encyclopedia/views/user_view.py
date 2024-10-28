from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from encyclopedia.helpers import check_role


# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar o usuário da wiki
@api_view(['POST'])
@csrf_exempt
def create_user(request):
    username = request.data.get('email')
    email = request.data.get('email')
    password = request.data.get('password')
    city = request.data.get('city')
    name = request.data.get('name')

    if not email or not password or not name:
        return Response({"error": "É necessário fornecer o email, o nome e a senha!"}, status=status.HTTP_400_BAD_REQUEST)

    if models.User.objects.filter(email=email).exists():
        return Response({"error": "O email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

    user = models.User.objects.create_user(
        username=username,
        email=email,
        password=password,
        name = name,
        city = city,
    )
    serializer = serializers.UserSerializer(user)
    return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)

# Verificar autorização do usuário
@api_view(['POST'])
def check_login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({"error": "Email e a senha são obrigatórios!"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Busca o usuário pelo email
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        # Retorna erro se o usuário não for encontrado
        return Response({"error": "Email ou senha incorretos!"}, status=status.HTTP_401_UNAUTHORIZED)

    # Verifica se a senha fornecida corresponde à senha armazenada no banco (criptografada)
    if user.check_password(password):
        return Response({
            "id": user.id,
            "role": user.role
            }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Email ou senha incorretos!"}, status=status.HTTP_401_UNAUTHORIZED)

# Listar usuários com limite e ordenar por data de registro (mais recentes)
@api_view(['GET'])
def list_users(request, quantity=20):
    try:
        quantity = int(quantity)
    except ValueError:
        return Response({"error": "Quantidade inválida."}, status=status.HTTP_400_BAD_REQUEST)
    
    users = models.User.objects.order_by('-date_joined')[:quantity]
    serializer = serializers.UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Obter usuário por email
@api_view(['GET'])
def get_user_by_email(request, email):
    try:
        user = models.User.objects.get(email=email)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except models.User.DoesNotExist:
        return Response({"error": "O Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    
# Obter usuário por ID
@api_view(['GET'])
def get_user_by_id(request, id):
    try:
        user = models.User.objects.get(id=id)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except models.User.DoesNotExist:
        return Response({"error": "O Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

# Deletar um usuário da wiki usando o ID do usuário
@api_view(['DELETE'])
def delete_user(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    user.delete()
    return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

# Atualizar informações de um usuário da wiki usando o ID do usuário
@api_view(['PUT'])
def update_user(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    data = request.data.copy()
    data.pop('password', None)  # Remove 'password' se estiver presente
    serializer = serializers.UserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
def update_user_password(request, user_id):
    # Obtém o usuário ou retorna 404 se não encontrado
    user = get_object_or_404(models.User, id=user_id)
    
    # Extrai as senhas do corpo da requisição
    password = request.data.get('password')
    new_password = request.data.get('new_password')
    
    # Verifica se a senha atual foi fornecida
    if not password:
        return Response("A senha atual é necessária.", status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se a nova senha foi fornecida
    if not new_password:
        return Response("A nova senha não pode ser vazia.", status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se a senha atual está correta
    if not user.check_password(password):
        return Response("A senha fornecida está incorreta.", status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se a nova senha é diferente da senha atual
    if user.check_password(new_password):
        return Response("A nova senha não pode ser igual à anterior.", status=status.HTTP_400_BAD_REQUEST)
    
    # Atualiza a senha do usuário de forma segura
    user.set_password(new_password)
    user.save()
    
    return Response("Senha atualizada com sucesso.", status=status.HTTP_200_OK)