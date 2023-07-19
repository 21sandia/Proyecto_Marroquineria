from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_product(request):
    queryset = Product.objects.all().order_by('name')
    serializer = ProductSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'No hay productos registrados',
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
products = Product.objects.order_by('name')

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Verificar si el producto ya existe
    name = serializer.validated_data['name']
    existing_product = Product.objects.filter(name=name).first()
    if existing_product:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'El producto ya existe', 'status': False})

    serializer.save()
    return Response(data={'code': status.HTTP_201_CREATED, 'message': 'Creado Exitosamente', 'status': True})
      

@api_view(['PATCH'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    serializer = ProductSerializer(product, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response (data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    product.delete()
    return Response (data={'code':status.HTTP_202_ACCEPTED, 'message':'Eliminado Exitosamente', 'status':True})