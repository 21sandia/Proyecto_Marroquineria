from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_sale(request):
    queryset = Sale.objects.all().order_by('date_sale')
    serializer = SaleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay ventas existentes',
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
def create_sale(request):
    try:
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        existing_sale = Sale.objects.filter(name=name).first()
        if existing_sale:
            return Response(data={'code': status.HTTP_200_OK, 'message': 'La venta ya existe', 'status': False})

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Creada Exitosamente', 'status': True})
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor: '+str(e), 'status': False})
    
@api_view(['PATCH'])
def update_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)

        serializer = SaleSerializer(sale, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 'message': 'Actualizada Exitosamente', 'status': True})

    except Role.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No encontrada', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor: ' + str(e), 'status': False})

@api_view(['DELETE'])
def delete_sale(request, pk):
    try:
        sale = Sale.objects.get(pk=pk)
        sale.delete()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Eliminada exitosamente', 'status': True})

    except Sale.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 'message': 'No encontrada', 'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 'message': 'Error de red', 'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Error del servidor', 'status': False})
