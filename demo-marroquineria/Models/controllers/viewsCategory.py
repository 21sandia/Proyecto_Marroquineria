from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_category(request):
    queryset = Category.objects.all().order_by('name')
    serializer = CategorySerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay categorías registradas',
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
def create_category(request):
    try:
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si la categoría ya existe
        name = serializer.validated_data['name']
        existing_category = Category.objects.filter(name=name).first()
        if existing_category:
            return Response(data={'code': status.HTTP_200_OK, 'message': 'Ya existe esta categoría', 'status': False})

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Categoría creada exitosamente', 'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})

@api_view(['PATCH'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Actualizado exitosamente', 'status': True})

    except Category.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 'message': 'No encontrado', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Eliminado exitosamente', 'status': True})

    except Category.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'Categoría No encontrada', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})

