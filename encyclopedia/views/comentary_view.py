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

# Criar um novo comentário (requer que o usuário esteja logado)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comentary(request):
    serializer = serializers.ComentarioSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Listar todos os comentários
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_comments(request):
    comentarios = models.Comentario.objects.all()
    serializer = serializers.ComentarioSerializer(comentarios, many=True)
    return Response(serializer.data)

# Deletar um comentário (requer login e ser Admin ou Staff) - usa o ID do comentário.
@api_view(['DELETE'])
@login_required(login_url='/login/')  # Garante que o usuário esteja logado
@user_passes_test(is_admin_or_staff)  # Verifica se o usuário é Admin ou Staff
def delete_comment(request, commentary_id):
    comentario = get_object_or_404(models.Comentario, id=commentary_id)
    comentario.delete()
    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)

# Atualizar um comentário (requer login e ser Admin ou Staff), além de usar o ID do comentário.
@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def update_comment(request, commentary_id):
    comentario = get_object_or_404(models.Comentario, id=commentary_id)
    serializer = serializers.ComentarioSerializer(
        comentario, data=request.data, partial=True, context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
