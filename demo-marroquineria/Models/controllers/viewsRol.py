from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_rol(request):
    queryset = Rol.objects.all().order_by('name')
    serializer = RolSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay roles registrados',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

@api_view(['POST'])
def create_rol(request):
    try:
        serializer = RolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        existing_rol = Rol.objects.filter(name=name).first()
        if existing_rol:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'El rol ya existe', 
                                  'status': False})

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Creado Exitosamente', 
                              'status': True})
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: '+str(e), 
                              'status': False})
    
@api_view(['PATCH'])
def update_rol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)

        serializer = RolSerializer(rol, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizado Exitosamente', 
                              'status': True})

    except Rol.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Rol No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: ' + str(e), 
                              'status': False})

@api_view(['DELETE'])
def delete_rol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)
        rol.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True})

    except Rol.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'Rol No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})


