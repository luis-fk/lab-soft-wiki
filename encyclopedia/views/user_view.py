from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models
from django.contrib.auth.hashers import check_password

# Função auxiliar para verificar se o usuário é Admin ou Staff
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# Criar o usuário da wiki
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    city = request.data.get('city')
    name = request.data.get('name')

    if not email or not password:
        return Response({"error": "É necessário fornecer o email e a senha!"}, status=status.HTTP_400_BAD_REQUEST)

    if models.User.objects.filter(email=email).exists():
        return Response({"error": "O email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

    user = models.User.objects.create_user(
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


# Listar todos os usuários da wiki ou um em específico.
@api_view(['GET'])
def list_user(request, id=None):
    if id is not None:
        try:
            user = models.User.objects.get(id=id)
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({"error": "O Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    # Se não houver 'id', retorna a lista de todos os usuários
    users = models.User.objects.all()
    serializer = serializers.UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
