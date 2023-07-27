from rest_framework.decorators import api_view
from rest_framework.response import Response
from requests.exceptions import RequestException
from rest_framework import status
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_product(request):
    queryset = Product.objects.all().order_by('name')
    serializer = ProductSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay productos registrados',
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
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el producto ya existe
        name = serializer.validated_data['name']
        existing_product = Product.objects.filter(name=name).first()
        if existing_product:
            return Response(data={'code': status.HTTP_200_OK, 'message': 'El producto ya existe', 'status': False})

        # Agregar el código para enviar la imagen
        image = request.FILES.get('image')
        if image:
            serializer.validated_data['image'] = image

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Producto creado exitosamente', 'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})

@api_view(['PATCH'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Actualizado exitosamente', 'status': True})

    except Product.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 'message': 'No encontrado', 'status': False})

    except RequestException:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Eliminado exitosamente', 'status': True})

    except Product.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No encontrado', 'status': False})

    except RequestException:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})
