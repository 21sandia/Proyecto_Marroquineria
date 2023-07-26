from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_Status_g(request):
    queryset = Status_g.objects.all().order_by('name')
    serializer = StatusSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
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
    # Verifica si el estado ya existe
    existing_status = Status_g.objects.filter(**request.data).first()
    if existing_status:
        # Si el estado ya existe, envía el mensaje
        serializer = StatusSerializer(existing_status)
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'El objeto ya existe.', 'status': False, 'data': serializer.data})

    # Si el estado no existe, lo guarda
    serializer = StatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Creado Exitosamente', 'status': True, 'data': serializer.data})      

@api_view(['PATCH'])
def update_Status_g(request, pk):
    try:
        status_g = Status_g.objects.get(pk=pk)
    except Status_g.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No Encontrado', 'status': True})
    
    serializer = StatusSerializer(status_g, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Actualizado Exitosamente', 'status': True})

@api_view(['DELETE'])
def delete_Status_g(request, pk):
    try:
        status_g = Status_g.objects.get(pk=pk)
    except Status_g.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No Encontrado', 'status': True})
    
    status_g.delete()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Eliminado Exitosamente', 'status': True})
