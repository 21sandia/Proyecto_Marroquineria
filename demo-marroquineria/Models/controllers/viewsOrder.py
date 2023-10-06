from decimal import Decimal
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from ..models import Orders, OrderItems, Products, States, Users
from ..serializers import *

from django.db.models import Sum


@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    address = request.data.get('address')
    # state_id = request.data.get('fk_id_state') 

    # Obtener el estado "pedido en proceso" de la tabla States
    desired_state = States.objects.filter(name='Pedido en Proceso').first()

    if not desired_state:
        return Response({'code': status.HTTP_400_BAD_REQUEST,
                         'message': 'El estado "Pedido en Proceso" no existe en la base de datos',
                         'status': False,
                         'data': None})

    # Recuperar los artículos de la cesta del usuario
    cart_items = Cart_items.objects.filter(fk_id_cart__fk_id_user=user_id)

    # Comprobar si la cesta está vacía
    if not cart_items:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'No hay productos en el carrito',
                         'status': False,
                         'data': None})

    # Calcular el total_price del pedido
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.fk_id_product.price_sale * cart_item.quantity

    # Crear el pedido y los artículos del pedido
    order_data = {'fk_id_user': user_id, 'address': address, 'total_price': total_price, 'fk_id_state': desired_state.id}
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()

        # Añadir los cart_items al pedido
        order_items = []
        for cart_item in cart_items:
            order_item_data = {'fk_id_order': order, 'fk_id_product': cart_item.fk_id_product, 'quantity': cart_item.quantity, 'price': cart_item.total_price}
            order_items.append(OrderItems(**order_item_data))

        # Crear los elementos de order con bulk_create
        OrderItems.objects.bulk_create(order_items)

        # Borrar el carrito del usuario
        cart_items.delete()

        return Response({'code': status.HTTP_200_OK,
                        'message': 'La orden se creó exitosamente',
                        'status': True,
                        'data': order_serializer.data})


@api_view(['PATCH'])
def edit_order(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'La orden no existe',
                         'status': False,
                         'data': None})

    # Verificar si se proporciona un nuevo estado
    new_state_id = request.data.get('fk_id_state')
    if new_state_id is not None:
        # Verificar si ya existe un estado con el mismo nombre
        existing_state = States.objects.filter(Q(name=new_state_id) & ~Q(id=order.fk_id_state.id)).first()
        if existing_state:
            return Response({'code': status.HTTP_200_OK,
                             'message': 'Ya existe un estado con ese nombre en la base de datos',
                             'status': False,
                             'data': None})
        
        try:
            new_state = States.objects.get(id=new_state_id)
        except States.DoesNotExist:
            return Response({'code': status.HTTP_200_OK,
                             'message': 'El estado especificado no existe',
                             'status': False,
                             'data': None})
        
        order.fk_id_state = new_state  # Actualizar el estado de la orden
        order.save()
        
        # Formatea la fecha en el formato deseado
        formatted_date = order.date.strftime('%Y-%m-%d')
        
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'El estado de la orden se actualizó exitosamente',
            'status': True,
            'data': {
                'id': order.id,
                'date': formatted_date,
                # Agrega otros campos de la orden aquí según sea necesario
            }
        }
        
        return Response(response_data)

    return Response({'code': status.HTTP_200_OK,
                     'message': 'No se especificaron datos para actualizar',
                     'status': True,
                     'data': None})




@api_view(['GET'])
def list_products_order(request):
    # Obtener los parámetros de filtrado de la solicitud
    user_id = request.query_params.get('user_id', None)
    state_id = request.query_params.get('state_id', None)
    min_total_sale = request.query_params.get('min_total_sale', None)
    max_total_sale = request.query_params.get('max_total_sale', None)
    start_date_str = request.query_params.get('start_date', None)
    end_date_str = request.query_params.get('end_date', None)
    order_id = request.query_params.get('order_id', None)

    # ... (código de conversión de fechas y filtrado)
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
    order_query = Q()
    if user_id:
        order_query &= Q(fk_id_user=user_id)
    if state_id:
        order_query &= Q(fk_id_state=state_id)
    if min_total_sale:
        order_query &= Q(total_price__gte=min_total_sale)
    if max_total_sale:
        order_query &= Q(total_price__lte=max_total_sale)
    if start_date:
        order_query &= Q(date__gte=start_date)
    if end_date:
        order_query &= Q(date__lte=end_date)
    if order_id:
        order_query &= Q(id=order_id)

    # Obtener todas las órdenes que cumplen con los filtros
    #orders = Orders.objects.filter(order_query)

    # Ordena las ordenes por fecha de la más antigua a la más nueva
    orders = Orders.objects.filter(order_query).order_by('date')

    response_data = []

    for order in orders:
        products = OrderItems.objects.filter(fk_id_order=order)
        total_quantity = products.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_price = products.aggregate(total_price=Sum('price'))['total_price']

        product_data = []

        for product in products:
            product_obj = product.fk_id_product
            product_item = {
                'product_id': product_obj.id,
                'product_name': product_obj.name,
                'quantity': product.quantity,
                'price_unit':product_obj.price_sale,
                'total_units_price':product.price,
            }
            product_data.append(product_item)

        order_data = {
            'order_id': order.id,
            'user_id': order.fk_id_user.id,
            'user_name': order.fk_id_user.fk_id_people.name,
            'user_document': order.fk_id_user.fk_id_people.document,
            'address': order.address,
            'date': order.date.strftime('%Y-%m-%d'),  # Agregar la fecha de la orden en el formato deseado
            'total_quantity': total_quantity,
            'total_price':total_price,
            'phone_user':order.fk_id_user.fk_id_people.phone,
            'products': product_data,
            'order_state': {
                'id': order.fk_id_state.id,
                'name': order.fk_id_state.name,
            },
        }

        response_data.append(order_data)

    if response_data:
        response = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada exitosamente',
            'data': response_data
        }
    else:
        response = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No hay información disponible',
            'data': []
        }

    return Response(response)




@api_view(['GET'])
def list_products_order_user(request):
    # Obtener los parámetros de filtrado de la solicitud
    user_id = request.query_params.get('user_id', None)
    state_id = request.query_params.get('state_id', None)
    rol_name = request.query_params.get('rol', None)
    min_total_sale = request.query_params.get('min_total_sale', None)
    max_total_sale = request.query_params.get('max_total_sale', None)
    start_date_str = request.query_params.get('start_date', None)
    end_date_str = request.query_params.get('end_date', None)
    order_id = request.query_params.get('order_id', None)

    # ... (código de conversión de fechas y filtrado)
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
    order_query = Q()
    if user_id:
        order_query &= Q(fk_id_user=user_id)
    if state_id:
        order_query &= Q(fk_id_state=state_id)
    if min_total_sale:
        order_query &= Q(total_price__gte=min_total_sale)
    if max_total_sale:
        order_query &= Q(total_price__lte=max_total_sale)
    if start_date:
        order_query &= Q(date__gte=start_date)
    if end_date:
        order_query &= Q(date__lte=end_date)
    if order_id:
        order_query &= Q(id=order_id)

    if user_id:
        order_query &= Q(fk_id_user=user_id)

        # Verifica si el usuario tiene el rol especificado por nombre
        if rol_name:
            try:
                user = Users.objects.get(id=user_id)
                rol = Rol.objects.get(name=rol_name)
                if user.fk_id_rol != rol:
                    response_data = {
                        'code': status.HTTP_404_NOT_FOUND,
                        'message': 'El usuario no tiene el rol especificado',
                        'status': False
                    }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            except Users.DoesNotExist:
                response_data = {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'No se encontró el usuario con el ID especificado',
                    'status': False
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            except Rol.DoesNotExist:
                response_data = {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'No se encontró el rol con el nombre especificado',
                    'status': False
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    orders = Orders.objects.filter(order_query).order_by('date')

    response_data = []

    for order in orders:
        products = OrderItems.objects.filter(fk_id_order=order)
        total_quantity = products.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_price = products.aggregate(total_price=Sum('price'))['total_price']

        product_data = []

        for product in products:
            product_obj = product.fk_id_product
            product_item = {
                'product_id': product_obj.id,
                'product_name': product_obj.name,
                'quantity': product.quantity,
                'price_unit':product_obj.price_sale,
                'total_units_price':product.price,
            }
            product_data.append(product_item)

        order_data = {
            'order_id': order.id,
            'user_id': order.fk_id_user.id,
            'user_name': order.fk_id_user.fk_id_people.name,
            'user_document': order.fk_id_user.fk_id_people.document,
            'address': order.address,
            'date': order.date.strftime('%Y-%m-%d'),  # Agregar la fecha de la orden en el formato deseado
            'total_quantity': total_quantity,
            'total_price':total_price,
            'phone_user':order.fk_id_user.fk_id_people.phone,
            'products': product_data,
            'order_state': {
                'id': order.fk_id_state.id,
                'name': order.fk_id_state.name,
            },
        }

        response_data.append(order_data)

    if response_data:
        response = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada exitosamente',
            'data': response_data
        }
    else:
        response = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No hay información disponible',
            'data': []
        }

    return Response(response)
