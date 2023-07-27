from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException
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
    try:
        serializer = StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Verifica si el estado ya existe
        name = serializer.validated_data['name']
        existing_status_g = Status_g.objects.filter(name=name).first()
        # Si el estado ya existe, envía el mensaje
        if existing_status_g:
            return Response(data={'code': status.HTTP_200_OK, 'message': 'El estado ya existe', 'status': False})
        # Si el estado no existe, lo guarda
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Estado Creado Exitosamente', 'status': True})
    
    except RequestException:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor: '+str(e), 'status': False})
          

@api_view(['PATCH'])
def update_Status_g(request, pk):
    try:
        status_g = Status_g.objects.get(pk=pk)

        serializer = StatusSerializer(status_g, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Estado Actualizado exitosamente', 'status': True})

    except Status_g.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 'message': 'No encontrado', 'status': False})

    except RequestException:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})
    

@api_view(['DELETE'])
def delete_Status_g(request, pk):
    try:
        status_g = Status_g.objects.get(pk=pk)
        status_g.delete()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Se ha Eliminado exitosamente', 'status': True})

    except Status_g.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'Estado No encontrado', 'status': False})

    except RequestException:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})


