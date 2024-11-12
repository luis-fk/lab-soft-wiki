from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from encyclopedia import serializers
from encyclopedia import models
from encyclopedia.helpers import check_role


# CRUD para Denuncia

# Criar uma nova denúncia
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from encyclopedia.models import Denuncia, Endereco, User
from encyclopedia.serializers import DenunciaSerializer

# Criar uma nova denúncia, instanciando já o endereço dela
@api_view(['POST'])
def create_denuncia(request):
    # Extrai os dados do JSON recebido
    user_id = request.data.get('id')
    state = request.data.get('state')
    city = request.data.get('city')
    district = request.data.get('district')
    street = request.data.get('street')
    number = request.data.get('number')
    text = request.data.get('text')

    # Verifica se o usuário existe
    user = get_object_or_404(User, id=user_id)

    # Cria o endereço com os dados fornecidos
    endereco = Endereco.objects.create(
        estado=state,
        cidade=city,
        bairro=district,
        rua=street,
        numero=number
    )

    # Cria a denúncia associada ao usuário e ao endereço
    denuncia = Denuncia.objects.create(
        text=text,
        user=user,
        endereco=endereco
    )

    # Serializa a denúncia para retornar a resposta
    serializer = DenunciaSerializer(denuncia)
    return Response("Denuncia criada com sucesso!", status=status.HTTP_201_CREATED)


# Listar todas as denúncias
@api_view(['GET'])
def list_denuncias(request):
    denuncias = models.Denuncia.objects.all()
    serializer = serializers.DenunciaSerializer(denuncias, many=True)
    return Response(serializer.data)

# Atualizar uma denúncia (usando o ID da denúncia)
@api_view(['PUT'])
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
def delete_denuncia(request, denuncia_id):
    if check_role(request):
        denuncia = get_object_or_404(models.Denuncia, id=denuncia_id)
        # Verifica se o usuário que está fazendo a exclusão é o autor da denúncia ou um administrador
        if request.user != denuncia.user and not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        denuncia.delete()
        return Response({"message": "Denuncia deleted successfully."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)