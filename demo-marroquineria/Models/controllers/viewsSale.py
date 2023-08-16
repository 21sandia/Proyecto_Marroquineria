from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests


# **Crea la venta junto con el detalle de venta**
@api_view(['POST'])
def create_sale_detail(request):
    state_id = request.data.get('state_id')
    people_id = request.data.get('people_id')
    products = request.data.get('products', [])
    
    # Validar que el estado y la persona existan
    try:
        state = States.objects.get(id=state_id)
    except States.DoesNotExist:
        return Response({"message": "Estado no encontrado."}, status=400)
    
    try:
        people = Peoples.objects.get(id=people_id)
    except Peoples.DoesNotExist:
        return Response({"message": "Persona no encontrada."}, status=400)
    
    # Guardar la venta
    sale_data = {
        'fk_id_state': state,
        'fk_id_people': people,
        'total_sale': 0,  # Será actualizada más adelante
    }
    sale_serializer = SaleSerializer(data=sale_data)
    if sale_serializer.is_valid():
        sale = sale_serializer.save()  # Crea la venta y la asigna a la variable 'sale'
    else:
        return Response(sale_serializer.errors, status=400)
    
    total_sale = 0
    
    # Guardar el detalle de la venta
    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')
        
        # Validar que el producto exista
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"message": "Producto no encontrado."}, status=400)
        
        price_unit = product.price_sale
        total_product = price_unit * quantity
        total_sale += total_product
        
        detail_data = {
            'fk_id_sale': sale,       # Asigna la venta creada anteriormente
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': price_unit,
            'total_product': total_product,
        }
        
        detail_serializer = DetailSaleSerializer(data=detail_data)
        if detail_serializer.is_valid():
            detail_serializer.save()  # Crea el detalle de venta
        else:
            return Response(detail_serializer.errors, status=400)
    
    # Actualizar el total de la venta
    sale.total_sale = total_sale
    sale_serializer = SaleSerializer(instance=sale, data={'total_sale': total_sale}, partial=True)
    if sale_serializer.is_valid():
        sale_serializer.save()  # Actualiza el total de la venta
    else:
        return Response(sale_serializer.errors, status=400)
    
    return Response(sale_serializer.data, status=201)  # Devuelve los datos de la venta creada


# **Lista los datos de venta junto con detalle venta**
@api_view(['GET'])
def list_sale_detail(request, sale_id):
    try:
        sale = Sales.objects.get(pk=sale_id)
    except Sales.DoesNotExist:
        return Response({"message": "Venta no encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
    sale_serializer = SaleSerializer(sale)
    
    # Obtener detalles de la venta asociados
    details = DetailSales.objects.filter(fk_id_sale=sale)
    if not details:
        return Response({"message": "Detalles de venta no encontrados."}, status=status.HTTP_404_NOT_FOUND)
    
    detail_serializer = DetailSaleSerializer(details, many=True)
    
    response_data = {
        "sale": sale_serializer.data,
        "details": detail_serializer.data,
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


# **Edita la venta junto con el detalle de venta**
@api_view(['POST'])
def edit_sale_detail(request):
    sale_id = request.data.get('sale_id')
    state_id = request.data.get('state_id')
    people_id = request.data.get('people_id')
    products = request.data.get('products', [])
    
    # Validate the existence of the sale
    try:
        sale = Sales.objects.get(id=sale_id)
    except Sales.DoesNotExist:
        return Response({"message": "Sale not found."}, status=400)
    
    # Validate the existence of the state and people
    try:
        state = States.objects.get(id=state_id)
    except States.DoesNotExist:
        return Response({"message": "State not found."}, status=400)
    
    try:
        people = Peoples.objects.get(id=people_id)
    except Peoples.DoesNotExist:
        return Response({"message": "People not found."}, status=400)
    
    # Update the sale entity
    sale.fk_id_state = state
    sale.fk_id_people = people
    
    # Calculate the total sale amount
    total_sale = 0
    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')
        
        # Validate the existence of the product
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({"message": "Product not found."}, status=400)
        
        price_unit = product.price_sale
        total_product = price_unit * quantity
        total_sale += total_product
    
    # Update the sale's total_sale attribute
    sale.total_sale = total_sale
    
    # Delete the existing detail records associated with the sale
    DetailSales.objects.filter(fk_id_sale=sale).delete()
    
    # Save the updated sale entity
    sale.save()
    
    
    # Save the edited detail records
    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')
        
        product = Products.objects.get(id=product_id)
        price_unit = product.price_sale
        total_product = price_unit * quantity
        
        detail_data = {
            'fk_id_sale': sale,
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': price_unit,
            'total_product': total_product,
        }
        
        detail_serializer = DetailSaleSerializer(data=detail_data)
        if detail_serializer.is_valid():
            detail_serializer.save()
        else:
            return Response(detail_serializer.errors, status=400)
    
    # Return the updated sale data
    sale_serializer = SaleSerializer(sale)
    return Response(sale_serializer.data, status=200)


@api_view(['DELETE'])
def delete_sale_detail(request, pk):
    try:
        sale = Sales.objects.get(pk=pk)
        
        # Eliminar los registros de detalles existentes asociados con la venta
        DetailSales.objects.filter(fk_id_sale=sale).delete()

        # Eliminar la venta
        sale.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminada exitosamente', 
                              'status': True})

    except Sales.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
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



# @api_view(['DELETE'])
# def delete_sale(request, pk):
#     try:
#         sale = Sales.objects.get(pk=pk)
#         sale.delete()

#         return Response(data={'code': status.HTTP_200_OK, 
#                               'message': 'Eliminada exitosamente', 
#                               'status': True})

#     except Sales.DoesNotExist:
#         return Response(data={'code': status.HTTP_404_NOT_FOUND, 
#                               'message': 'No encontrada', 
#                               'status': False})

#     except requests.ConnectionError:
#         return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
#                               'message': 'Error de red', 
#                               'status': False})

#     except Exception as e:
#         return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
#                               'message': 'Error del servidor', 
#                               'status': False})
