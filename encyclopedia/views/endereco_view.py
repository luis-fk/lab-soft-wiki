from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from encyclopedia import serializers
from encyclopedia import models

# CRUD para Endereco

# Criar um novo endereço
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_endereco(request):
    serializer = serializers.EnderecoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listar todos os endereços
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_enderecos(request):
    enderecos = models.Endereco.objects.all()
    serializer = serializers.EnderecoSerializer(enderecos, many=True)
    return Response(serializer.data)

# Atualizar um endereço (usando o ID do endereço)
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_endereco(request, endereco_id):
    endereco = get_object_or_404(models.Endereco, id=endereco_id)
    serializer = serializers.EnderecoSerializer(endereco, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Deletar um endereço (usando o ID do endereço)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_endereco(request, endereco_id):
    endereco = get_object_or_404(models.Endereco, id=endereco_id)
    endereco.delete()
    return Response({"message": "Endereco deleted successfully."}, status=status.HTTP_200_OK)
