
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_detailProd(request):
    queryset = DetailProd.objects.all().order_by('registration_date')
    serializer = DetailProdSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'No Disponible',
            'status': False
        }
        return Response(response_data)

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Consulta Realizada Exitosamente',
        'status': True,
        'data': serializer.data
    }
    return Response(response_data)

@api_view(['POST'])
def create_detailProd(request):
    serializer = DetailProdSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Creado Exitosamente', 'status':True})      

@api_view(['PATCH'])
def update_detailProd(request, pk):
    try:
        detail_prod = DetailProd.objects.get(pk=pk)
    except DetailProd.DoesNotExist:
        return Response(data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    serializer = DetailProdSerializer(detail_prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_detailProd(request, pk):
    try:
        detail_prod = DetailProd.objects.get(pk=pk)
    except DetailProd.DoesNotExist:
        return Response (data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    detail_prod.delete()
    return Response (data={'code':status.HTTP_202_ACCEPTED, 'message':'Eliminado Exitosamente', 'status':True})
