from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from encyclopedia import serializers
from encyclopedia import models
from encyclopedia.helpers import check_role
from django.utils import timezone


@api_view(['POST'])
def create_comentary(request):
    # Adiciona o campo created_at ao request data com a data e hora atuais
    request.data['created_at'] = timezone.now()

    # Verifica se o user_id foi fornecido
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({"error": "O 'user_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Tenta encontrar o usuário, retornando erro caso não exista
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return Response({"error": "O Usuário não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica se o article_id foi fornecido
    article_id = request.data.get('article_id')
    if not article_id:
        return Response({"error": "O 'article_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Tenta encontrar o artigo, retornando erro caso não exista
    try:
        article = models.Artigo.objects.get(id=article_id)
    except models.Artigo.DoesNotExist:
        return Response({"error": "O Artigo não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica se o texto foi fornecido
    text = request.data.get('text')
    if not text:
        return Response({"error": "O 'text' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Serializa os dados recebidos e cria o comentário
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

# Listar todos os comentários de um artigo por ID de artigo.
@api_view(['GET'])
def list_comments_by_article(request, article_id):
    try:
        # Converte o article_id para inteiro
        article_id = int(article_id)
    except ValueError:
        return Response({"error": "ID do Artigo inválido."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifica se o artigo existe
    try:
        models.Artigo.objects.get(id=article_id)
    except models.Artigo.DoesNotExist:
        return Response({"error": "O Artigo não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Busca pelos comentários relacionados ao ID do artigo
    comentarios = models.Comentario.objects.filter(article_id=article_id)

    # Verifica se existem comentários
    if comentarios.exists():
        serializer = serializers.ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Nenhum comentário foi encontrado."}, status=status.HTTP_200_OK)

    
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






