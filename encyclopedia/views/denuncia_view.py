from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from . import models
from . import serializers

# CRUD para Denuncia

# Criar uma nova denúncia
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_denuncia(request):
    serializer = serializers.DenunciaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Define o usuário logado como o autor da denúncia
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listar todas as denúncias
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_denuncias(request):
    denuncias = models.Denuncia.objects.all()
    serializer = serializers.DenunciaSerializer(denuncias, many=True)
    return Response(serializer.data)

# Atualizar uma denúncia (usando o ID da denúncia)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(models.Denuncia, id=denuncia_id)

    # Verifica se o usuário que está fazendo a atualização é o autor da denúncia
    if request.user != denuncia.user:
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.DenunciaSerializer(denuncia, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Deletar uma denúncia (usando o ID da denúncia)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_denuncia(request, denuncia_id):
    denuncia = get_object_or_404(models.Denuncia, id=denuncia_id)

    # Verifica se o usuário que está fazendo a exclusão é o autor da denúncia ou um administrador
    if request.user != denuncia.user and not request.user.is_staff:
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    denuncia.delete()
    return Response({"message": "Denuncia deleted successfully."}, status=status.HTTP_200_OK)