from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_sale(request):
    queryset = Sale.objects.all().order_by('date_sale')
    serializer = SaleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'No hay ventas existentes',
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
def create_sale(request):
    serializer = SaleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Creado Exitosamente', 'status':True})      

@api_view(['PATCH'])
def update_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response(data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    serializer = SaleSerializer(sale, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
    except Sale.DoesNotExist:
        return Response (data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    sale.delete()
    return Response (data={'code':status.HTTP_202_ACCEPTED, 'message':'Eliminado Exitosamente', 'status':True})