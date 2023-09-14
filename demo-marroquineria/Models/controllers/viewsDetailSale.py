from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from ..models import *
from ..serializers import *
import requests


@api_view(['POST'])
def create_sale_detail(request):
    # Obtener los datos de la solicitud
    state_id = request.data.get('fk_id_state')
    people_id = request.data.get('fk_id_people')
    products = request.data.get('products', [])

    # Verificar si se proporcionaron valores para los campos state_id y people_id
    state = None
    if state_id:
        try:
            state = States.objects.get(id=state_id)
        except States.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Estado no encontrado.",
                "status": False
            })

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

    # Calcular el total de la venta
    total_sale = sum(detail['total_product'] for detail in detail_data_list)

    # Actualizar el total de la venta
    sale.total_sale = total_sale
    sale_serializer = SaleSerializer(instance=sale, data={'total_sale': total_sale}, partial=True)
    if sale_serializer.is_valid():
        sale_serializer.save()
    else:
        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Envía el correo electrónico de notificación
    subject = 'Comprobante de venta'
    message = f'Se ha creado una nueva venta con número de factura: {sale.id}.\n\n'
    message += 'Detalles de la compra:\n'
    for product_data, detail in zip(products, detail_data_list):
        product_id = product_data.get('product_id')
        quantity = detail['quantity']
        product = Products.objects.get(id=product_id)
        subtotal_product = detail['total_product']
        message += f'Producto: {product.name}, Cantidad: {quantity}, Precio unitario: {product.price_sale}, Subtotal: {subtotal_product}\n'
    from_email = 'ecommerce.marquetp@gmail.com' 
    recipient_list = [people.email]  # Cambia esto por la dirección de correo del cliente

    send_mail(subject, message, from_email, recipient_list)

    return Response({
        "code": status.HTTP_200_OK,
        "message": "Venta creada exitosamente. Se ha enviado un correo de notificación.",
        "status": True,
        "data": sale_serializer.data
    })


# **Lista los datos de venta junto con detalle venta**
from django.db.models import F

@api_view(['GET'])
def list_sale_detail(request):
    # Obtener los parámetros de filtrado de la solicitud
    customer_id = request.query_params.get('customer_id', None)
    state_id = request.query_params.get('state_id', None)
    min_total_sale = request.query_params.get('min_total_sale', None)
    max_total_sale = request.query_params.get('max_total_sale', None)
    start_date_str = request.query_params.get('start_date', None)
    end_date_str = request.query_params.get('end_date', None)

    # Convertir las fechas en objetos datetime si se proporcionan
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = None

    # Filtrar ventas según los parámetros proporcionados
    sales_query = Q()
    if customer_id:
        sales_query &= Q(fk_id_people=customer_id)
    if state_id:
        sales_query &= Q(fk_id_state=state_id)
    if min_total_sale:
        sales_query &= Q(total_sale__gte=min_total_sale)
    if max_total_sale:
        sales_query &= Q(total_sale__lte=max_total_sale)
    if start_date:
        sales_query &= Q(date__gte=start_date)
    if end_date:
        sales_query &= Q(date__lte=end_date)

    sales = Sales.objects.filter(sales_query)

    if not sales:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "No hay ventas registradas.",
            "status": True
        })

    response_data = []

    for sale in sales:
        # Obtener los datos de la persona, producto y estado
        person_data = Peoples.objects.filter(id=sale.fk_id_people_id).values('name', 'document', 'email').first()
        product_data = DetailSales.objects.filter(fk_id_sale_id=sale.id).values('fk_id_prod__id', 'fk_id_prod__name')
        state_data = States.objects.filter(id=sale.fk_id_state_id).values('id', 'name').first()

        sale_serializer = SaleSerializer(sale)

        sale_data = {
            "sale": sale_serializer.data,
            "person": person_data,
            "state": state_data,
            "products": product_data,
        }

        response_data.append(sale_data)

    return Response({
        "code": status.HTTP_200_OK,
        "message": "Consulta realizada exitosamente.",
        "status": True,
        "data": response_data  # Agrega el contenido de la respuesta aquí
    })


# **Edita la venta junto con el detalle de venta**
@api_view(['PATCH'])
def edit_sale_detail(request, pk):
    # Obtén los datos de la solicitud
    state_id = request.data.get('fk_id_state')
    people_id = request.data.get('fk_id_people')
    products = request.data.get('products', [])
    
    # Verificar si la venta existe
    try:
        sale = Sales.objects.get(pk=pk)
    except Sales.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Venta no encontrada.",
            "status": False
        })
    
    # Validar si el estado y la persona existen
    try:
        state = States.objects.get(id=state_id)
    except States.DoesNotExist:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Estado no encontrado.",
            "status": False
        })
    
    try:
        people = Peoples.objects.get(id=people_id)
    except Peoples.DoesNotExist:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Persona no encontrada.",
            "status": False
        })
    
    # Actualizar la entidad de venta
    sale.fk_id_state = state
    sale.fk_id_people = people
    
    # Calcular el monto total de la venta
    total_sale = 0
    detail_data_list = []
    
    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')
        
        # Validar si el producto existe
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Producto no encontrado.",
                "status": False
            })
        
        price_unit = product.price_sale
        total_product = price_unit * quantity
        total_sale += total_product
        
        detail_data = {
            'fk_id_sale': sale,
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': price_unit,
            'total_product': total_product,
        }
        
        detail_data_list.append(detail_data)
    
    # Actualizar el atributo total_sale de la venta
    sale.total_sale = total_sale
    
    # Eliminar los registros de detalles existentes asociados con la venta
    DetailSales.objects.filter(fk_id_sale=sale).delete()
    
    # Guardar la entidad de venta actualizada
    sale.save()
    
    # Crear detalles de venta en masa
    DetailSales.objects.bulk_create([DetailSales(**data) for data in detail_data_list])
    
    # Devolver los datos actualizados de la venta
    sale_serializer = SaleSerializer(sale)
    return Response({
        "code": status.HTTP_200_OK,
        "message": "Venta actualizada exitosamente.",
        "status": True,
        "data": sale_serializer.data
    })


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
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})



