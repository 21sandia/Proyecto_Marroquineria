"""from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_carts(request):
    queryset = Carts.objects.all()
    serializer = CartsSerializer(queryset, many=True)
    response_data = {
        'code': 'HTTP_200_OK',
        'message': 'Consulta Realizada Exitosamente',
        'status': True,
        'data': serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK) 

@api_view(['POST'])
def create_carts(request):
    serializer = CartsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Creado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_carts(request, pk):
    try:
        carts = Carts.objects.get(pk=pk)
    except Carts.DoesNotExist:
        return Response(data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = CartsSerializer(carts, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Actualizado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_carts(request, pk):
    try:
        carts = Carts.objects.get(pk=pk)
    except Carts.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    carts.delete()
    return Response (data={'code':'HTTP_201_CONTENT', 'message':'Eliminado Exitosamente', 'status':True}, status=status.HTTP_204_NO_CONTENT)
"""