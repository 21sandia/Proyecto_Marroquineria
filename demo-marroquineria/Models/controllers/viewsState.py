from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_States(request):
    queryset = States.objects.all().order_by('id')
    serializer = StateSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay estados registrados',
                         'status': True}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

@api_view(['POST'])
def create_States(request):
    try:
        serializer = StateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Verifica si el estado ya existe
        name = serializer.validated_data['name']
        existing_states = States.objects.filter(name=name).first()
        # Si el estado ya existe, envía el mensaje
        if existing_states:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'El estado ya existe', 
                                  'status': True})
        # Si el estado no existe, lo guarda
        serializer.save()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Estado Creado Exitosamente', 
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
def update_States(request, pk):
    try:
        states = States.objects.get(pk=pk)

        # Obtén el nombre enviado en los datos del request
        name = request.data.get('name')

        # Verifica si el nuevo nombre ya existe en la base de datos
        if name != states.name:
            exist_states = States.objects.filter(name=name).first()
            if exist_states:
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'message': 'El estado con este nombre ya existe',
                        'status': True,
                        'data': None})

        serializer = StateSerializer(states, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Estado Actualizado exitosamente', 
                              'status': True})

    except States.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})
    

@api_view(['DELETE'])
def delete_States(request, pk):
    try:
        states = States.objects.get(pk=pk)
        states.delete()

        return Response(data={'code': status.HTTP_200_OK,
                              'message': 'Se ha Eliminado exitosamente', 
                              'status': True})

    except States.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Estado No encontrado', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'No se puede eliminar este dato mientras esté en uso', 
                              'status': False})


