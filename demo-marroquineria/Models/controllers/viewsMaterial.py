from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests


@api_view(['POST'])
def create_material(request):
    try:
        serializer = MaterialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        existing_material = Materials.objects.filter(name=name).first()
        if existing_material:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'El material ya existe', 
                                  'status': False,
                                  'data': []
                                  })

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Creado Exitosamente', 
                              'status': True,
                              'data': []
                              })
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: '+str(e), 
                              'status': False,
                              'data': []
                              })

    

@api_view(['GET'])
def list_material(request):
    queryset = Materials.objects.all().order_by('name')
    serializer = MaterialSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay materiales registrados',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

    
@api_view(['PATCH'])
def update_material(request, pk):
    try:
        material = Materials.objects.get(pk=pk)

        serializer = MaterialSerializer(material, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Material actualizado Exitosamente', 
                              'status': True,
                              'data': []
                              })

    except Materials.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Material No encontrado', 
                              'status': False,
                              'data': []
                              })

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: ' + str(e), 
                              'status': False,
                              'data': []
                              })

@api_view(['DELETE'])
def delete_material(request, pk):
    try:
        material = Materials.objects.get(pk=pk)
        material.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True,
                              'data': []
                              })

    except Materials.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'Material No encontrado', 
                              'status': False,
                              'data': []
                              })

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })

    except Exception as e:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se puede eliminar este dato mientras esté en uso', 
                              'status': False,
                              'data': []})


