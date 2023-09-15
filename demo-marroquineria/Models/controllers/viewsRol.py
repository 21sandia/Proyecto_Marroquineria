from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Rol
from ..serializers import *
import requests


def crear_roles_iniciales():
    roles_iniciales = ["Administrador", "Vendedor", "Repartidor", "Cliente"]

    for rol_nombre in roles_iniciales:
        Rol.objects.get_or_create(name=rol_nombre)


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
                                  'status': False
                                  })

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Creado Exitosamente', 
                              'status': True,
                              'data':[name]
                              })
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data':[]
                              })
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: '+str(e), 
                              'status': False,
                              'data':[]
                              })

    

@api_view(['GET'])
def list_rol(request):
    queryset = Rol.objects.all().order_by('id')
    serializer = RolSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay roles registrados',
                         'status': False,
                         'data':[]}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

    
@api_view(['PATCH'])
def update_rol(request, pk):
    try:
        rol = Rol.objects.get(pk=pk)

        # Obtén el nombre enviado en los datos del request
        name = request.data.get('name')

        # Verifica si el nuevo nombre ya existe en la base de datos, excluyendo la categoría actual
        if name != rol.name:
            exist_rol = Rol.objects.filter(name=name).first()
            if exist_rol:
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'message': f'El tipo de producto con el nombre {rol.name} ya existe',
                        'status': True,
                        'data': None
                        })

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
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se puede eliminar este dato mientras esté en uso', 
                              'status': False})


