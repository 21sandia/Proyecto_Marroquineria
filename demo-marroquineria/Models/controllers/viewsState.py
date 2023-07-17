from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_Status_g(request):
    queryset = Status_g.objects.all()
    serializer = StatusSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'No hay estados registrados',
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
def create_Status_g(request):
    serializer = StatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Creado Exitosamente', 'status':True})      

@api_view(['PATCH'])
def update_Status_g(request, pk):
    try:
        Status = Status.objects.get(pk=pk)
    except Status.DoesNotExist:
        return Response(data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    serializer = StatusSerializer(Status, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_201_CREATED, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_Status_g(request, pk):
    try:
        Status_g = Status_g.objects.get(pk=pk)
    except Status_g.DoesNotExist:
        return Response (data={'code':status.HTTP_500_INTERNAL_SERVER_ERROR, 'message':'No Encontrado', 'status':True})
    
    Status_g.delete()
    return Response (data={'code':status.HTTP_202_ACCEPTED, 'message':'Eliminado Exitosamente', 'status':True})