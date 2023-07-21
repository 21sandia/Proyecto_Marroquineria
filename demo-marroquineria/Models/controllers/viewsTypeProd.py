from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_type_prod(request):
    queryset = TypeProd.objects.all().order_by('name')
    serializer = TypeProdSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay tipos de productos registrados',
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
def create_type_prod(request):
    serializer = TypeProdSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Verificar si el tipo de producto ya existe
    name = serializer.validated_data['name']
    existing_type = TypeProd.objects.filter(name=name).first()
    if existing_type:
        return Response(data={'code': status.HTTP_200_OK, 'message': 'El tipo de producto ya existe', 'status': False})

    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Creado Exitosamente', 'status': True})
      

@api_view(['PATCH'])
def update_type_prod(request, pk):
    try:
        type_prod = TypeProd.objects.get(pk=pk)
    except TypeProd.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 'message':'No Encontrado', 'status':True})
    
    serializer = TypeProdSerializer(type_prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_200_OK, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_type_prod(request, pk):
    try:
        type_prod = TypeProd.objects.get(pk=pk)
    except TypeProd.DoesNotExist:
        return Response (data={'code':status.HTTP_200_OK, 'message':'No Encontrado', 'status':True})
    
    type_prod.delete()
    return Response (data={'code':status.HTTP_200_OK, 'message':'Eliminado Exitosamente', 'status':True})