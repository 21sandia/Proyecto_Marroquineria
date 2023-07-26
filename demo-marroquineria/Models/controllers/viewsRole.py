from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_role(request):
    queryset = Role.objects.all().order_by('name')
    serializer = RoleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay roles registrados',
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
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    name = serializer.validated_data['name']
    existing_role = Role.objects.filter(name=name).first()
    if existing_role:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'El rol ya existe', 'status': False})

    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Creado Exitosamente', 'status': True})

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No Encontrado', 'status': True})
    
    serializer = RoleSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Actualizado Exitosamente', 'status': True})

@api_view(['DELETE'])
def delete_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No Encontrado', 'status': True})
    
    role.delete()
    return Response(data={'code': status.HTTP_200_OK, 'message': 'Eliminado Exitosamente', 'status': True})
