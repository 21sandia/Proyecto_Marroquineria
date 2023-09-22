from decimal import Decimal
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from ..models import Orders, OrderItems, Products, States, Users
from ..serializers import *

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    address = request.data.get('address')
    state_id = request.data.get('fk_id_state') 

    # Recuperar los artículos de la cesta del usuario
    cart_items = Cart_items.objects.filter(fk_id_cart__fk_id_user=user_id)

    # Comprobar si la cesta está vacía
    if not cart_items:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'No hay productos en el carrito',
                         'status': True,
                         'data': None})

    # Calcular el total_price del pedido
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.fk_id_product.price_sale * cart_item.quantity

    # Crear el pedido y los artículos del pedido
    order_data = {'fk_id_user': user_id, 'address': address, 'total_price': total_price, 'fk_id_state': state_id}
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()

        # Añadir los cart_items al pedido
        order_items = []
        for cart_item in cart_items:
            order_item_data = {'fk_id_order': order, 'fk_id_product': cart_item.fk_id_product, 'quantity': cart_item.quantity, 'price': cart_item.total_price}
            order_items.append(OrderItems(**order_item_data))

        # Crear los elementos de orden con bulk_create
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
                         'status': True,
                         'data': None})

    # Verificar si se proporciona un nuevo estado
    new_state_id = request.data.get('fk_id_state')
    if new_state_id is not None:
        # Verificar si ya existe un estado con el mismo nombre
        existing_state = States.objects.filter(Q(name=new_state_id) & ~Q(id=order.fk_id_state.id)).first()
        if existing_state:
            return Response({'code': status.HTTP_200_OK,
                             'message': 'Ya existe un estado con ese nombre en la base de datos',
                             'status': True,
                             'data': None})
        
        try:
            new_state = States.objects.get(id=new_state_id)
        except States.DoesNotExist:
            return Response({'code': status.HTTP_200_OK,
                             'message': 'El estado especificado no existe',
                             'status': True,
                             'data': None})
        
        order.fk_id_state = new_state  # Actualizar el estado de la orden
        order.save()
        return Response({'code': status.HTTP_200_OK,
                         'message': 'El estado de la orden se actualizó exitosamente',
                         'status': True,
                         'data': OrderSerializer(order).data})

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
    order_id = request.query_params.get('id', None)

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
        order_query &= Q(fk_id_people=user_id)
    if state_id:
        order_query &= Q(fk_id_state=state_id)
    if min_total_sale:
        order_query &= Q(total_sale__gte=min_total_sale)
    if max_total_sale:
        order_query &= Q(total_sale__lte=max_total_sale)
    if start_date:
        order_query &= Q(date__gte=start_date)
    if end_date:
        order_query &= Q(date__lte=end_date)
    if order_id:
        order_query &= Q(id=order_id)

    orderItem_data = OrderItems.objects.all()
    
    response_data = []

    for orderItem_obj in orderItem_data:
        order_id = orderItem_obj.fk_id_order.id  # Obtén la clave primaria del objeto Orders
        order_obj = Orders.objects.get(pk=order_id)

        
        product_id = orderItem_obj.fk_id_product.id
        product_obj = Products.objects.get(pk=product_id)
        
        state_id = order_obj.fk_id_state.id
        state_obj = States.objects.get(pk=state_id)
        
        user_id = order_obj.fk_id_user.id
        user_obj = Users.objects.get(pk=user_id)
        
        order_item_data = {

            'order_id': order_id,
            'user_id': user_id,
            'user_name': user_obj.fk_id_people.name,
            'user_document':user_obj.fk_id_people.document,
            'address':order_obj.address,
            'prod_items':{
            'product_id': product_id,
            'product_name': product_obj.name,
            'quantity': orderItem_obj.quantity,
            'price': "{:.2f}".format(Decimal(orderItem_obj.price)),
            },
            'order_state': {
                'id': state_id,
                'name': state_obj.name
            },  
        }
        
        response_data.append(order_item_data)

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