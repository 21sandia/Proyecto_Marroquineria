from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests

@api_view(['GET'])
def list_sale(request):
    queryset = Sales.objects.all().order_by('date_sale')
    serializer = SaleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay ventas existentes',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
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
        existing_sale = Sales.objects.filter(name=name).first()
        if existing_sale:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'La venta ya existe', 
                                  'status': False})

<<<<<<< Updated upstream
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Creada Exitosamente', 
                              'status': True})
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: '+str(e), 
                              'status': False})
=======
    people = None
    if people_id:
        try:
            people = Peoples.objects.get(id=people_id)
        except Peoples.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Persona no encontrada.",
                "status": False
            })

    # Crear una nueva venta
    sale_data = {
        'fk_id_state': state.id if state else None,
        'fk_id_people': people.id if people else None,
        'total_sale': 0,
    }
    sale_serializer = SaleSerializer(data=sale_data)
    if sale_serializer.is_valid():
        sale = sale_serializer.save()
    else:
        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    total_sale = 0
    detail_data_list = []

    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')

        # Verificar campos obligatorios en los detalles del producto
        if not product_id or not quantity:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Campos obligatorios faltantes en los detalles del producto: product_id, quantity.",
                "status": False
            })

        try:
            # Buscar el producto asociado
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "El producto no existe.",
                "status": False
            })

        # Calcular el subtotal del producto
        subtotal_product = product.price_sale * quantity
        total_sale += subtotal_product

        # Crear datos para el detalle del producto
        detail_data = {
            'fk_id_sale': sale,
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': product.price_sale,
            'total_product': subtotal_product,
        }
        detail_data_list.append(detail_data)

    # Crear detalles de venta en masa
    DetailSales.objects.bulk_create([DetailSales(**data) for data in detail_data_list])

    # Crear una ProductSale para cada producto vendido
    for detail_data in detail_data_list:
        product = detail_data['fk_id_prod']
        ProductSale.objects.create(product=product, sale=sale, quantity=detail_data['quantity'])

    # Actualizar el total de la venta
    sale.total_sale = total_sale
    sale_serializer = SaleSerializer(instance=sale, data={'total_sale': total_sale}, partial=True)
    if sale_serializer.is_valid():
        sale_serializer.save()
    else:
        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> Stashed changes
    
@api_view(['PATCH'])
def update_sale(request, pk):
    try:
        sale = Sales.objects.get(pk=pk)

        serializer = SaleSerializer(sale, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizada Exitosamente', 
                              'status': True})

    except Sales.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No encontrada', 
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
def delete_sale(request, pk):
    try:
        sale = Sales.objects.get(pk=pk)
        sale.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminada exitosamente', 
                              'status': True})

    except Sales.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No encontrada', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})
