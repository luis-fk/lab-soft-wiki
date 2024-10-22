from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models
from user_view import check_role

@api_view(['POST'])
def create_comentary(request):
    serializer = serializers.ComentarioSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Listar todos os comentários
@api_view(['GET'])
def list_comments(request):
    comentarios = models.Comentario.objects.all()
    serializer = serializers.ComentarioSerializer(comentarios, many=True)
    return Response(serializer.data)

# Deletar um comentário (requer login e ser Admin ou Staff) - usa o ID do comentário.
@api_view(['DELETE'])
def delete_comment(request, commentary_id):
    comentario = get_object_or_404(models.Comentario, id=commentary_id)
    comentario.delete()
    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)

# Atualizar um comentário (requer login e ser Admin ou Staff), além de usar o ID do comentário.
@api_view(['PUT'])
def update_comment(request, commentary_id):
    if check_role(request):
        comentario = get_object_or_404(models.Comentario, id=commentary_id)
        serializer = serializers.ComentarioSerializer(
            comentario, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "error": "O usuário não tem permissão para criar artigos."
        }, status=status.HTTP_400_BAD_REQUEST)
