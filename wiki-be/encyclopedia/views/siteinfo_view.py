from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from encyclopedia.models import SiteInfo
from encyclopedia.serializers import SiteInfoSerializer

# Listar todos os SiteInfos
@api_view(['GET'])
def list_siteinfos(request):
    site_id = request.query_params.get('id')  
    if site_id:  
        try:
            siteinfo = SiteInfo.objects.get(id=site_id) 
            serializer = SiteInfoSerializer(siteinfo) 
        except SiteInfo.DoesNotExist:
            return Response({"error": "SiteInfo with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
    else:
        siteinfos = SiteInfo.objects.all()  
        serializer = SiteInfoSerializer(siteinfos, many=True)

    return Response(serializer.data)

# Criar um novo SiteInfo
@api_view(['POST'])
def create_siteinfo(request):
    serializer = SiteInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("SiteInfo criado com sucesso.", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Atualizar um SiteInfo pelo ID
@api_view(['PUT'])
def update_siteinfo(request, siteinfo_id):
    siteinfo = get_object_or_404(SiteInfo, id=siteinfo_id)
    serializer = SiteInfoSerializer(siteinfo, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response("SiteInfo atualizado com sucesso.", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Deletar um SiteInfo pelo ID
@api_view(['DELETE'])
def delete_siteinfo(request, siteinfo_id):
    siteinfo = get_object_or_404(SiteInfo, id=siteinfo_id)
    siteinfo.delete()
    return Response({"message": "SiteInfo exluido com sucesso."}, status=status.HTTP_200_OK)
