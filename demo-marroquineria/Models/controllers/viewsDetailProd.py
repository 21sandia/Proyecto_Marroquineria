
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_detailProd(request):
    queryset = DetailProd.objects.all()
    serializer = Detail_prodSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_detailProd(request):
    serializer = Detail_prodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Creado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_detailProd(request, pk):
    try:
        detail_prod = DetailProd.objects.get(pk=pk)
    except DetailProd.DoesNotExist:
        return Response(data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = Detail_prodSerializer(detail_prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Actualizado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_detailProd(request, pk):
    try:
        detail_prod = DetailProd.objects.get(pk=pk)
    except DetailProd.DoesNotExist:
        return Response (data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    detail_prod.delete()
    return Response (data={'code':'HTTP_201_CREATED', 'message':'Elminado Exitosamente', 'status':True}, status=status.HTTP_204_NO_CONTENT)
