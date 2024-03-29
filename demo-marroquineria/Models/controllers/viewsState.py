from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_Status_g(request):
    queryset = States.objects.all().order_by('name')
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
    try:
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Verifica si el estado ya existe
        name = serializer.validated_data['name']
        existing_status_g = States.objects.filter(name=name).first()
        # Si el estado ya existe, envía el mensaje
        if existing_status_g:
            return Response(data={'code': status.HTTP_200_OK, 'message': 'El estado ya existe', 'status': False})
        # Si el estado no existe, lo guarda
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Estado Creado Exitosamente', 'status': True})
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor: '+str(e), 'status': False})
          

@api_view(['PATCH'])
def update_Status_g(request, pk):
    try:
        status_g = States.objects.get(pk=pk)

        serializer = StatusSerializer(States, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Estado Actualizado exitosamente', 'status': True})

    except States.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 'message': 'No encontrado', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})
    

@api_view(['DELETE'])
def delete_Status_g(request, pk):
    try:
        status_g = States.objects.get(pk=pk)
        status_g.delete()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Se ha Eliminado exitosamente', 'status': True})

    except States.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'Estado No encontrado', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})


