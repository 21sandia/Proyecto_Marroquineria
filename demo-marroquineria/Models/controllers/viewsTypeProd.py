from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_type_prod(request):
    queryset = TypeProds.objects.all().order_by('name')
    serializer = TypeProdSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay tipos de productos registrados',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

@api_view(['POST'])
def create_type_prod(request):
    try:
        serializer = TypeProdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si la categoría ya existe
        name = serializer.validated_data['name']
        existing_type_prod = TypeProds.objects.filter(name=name).first()
        if existing_type_prod:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'El tipo de producto Ya existe', 
                                  'status': False})

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Se ha creado exitosamente', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})


@api_view(['PATCH'])
def update_type_prod(request, pk):
    try:
        type_prod = TypeProds.objects.get(pk=pk)

        serializer = TypeProdSerializer(type_prod, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizado exitosamente', 
                              'status': True})

    except TypeProds.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})
    

@api_view(['DELETE'])
def delete_type_prod(request, pk):
    try:
        type_prod = TypeProds.objects.get(pk=pk)
        type_prod.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True})

    except TypeProds.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No se encontró', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})
    
    
