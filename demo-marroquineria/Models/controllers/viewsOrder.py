from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework import status
from ..models import *
from ..serializers import OrderSerializer, CartItemSerializer, OrderItemSerializer

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    address = request.data.get('address')
    state_id = request.data.get('fk_id_state') # Set the state ID according to your requirement

    # Retrieve the cart items for the user
    cart_items = Cart_items.objects.filter(fk_id_cart__fk_id_user=user_id)

    # Check if the cart is empty
    if not cart_items:
        return Response({'error': 'No hay productos en el carrito'}, status=400)

    # Calculate the total price of the order
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.fk_id_product.price_sale * cart_item.quantity

    # Create the order
    order_data = {'fk_id_user': user_id, 'address': address, 'total_price': total_price, 'fk_id_state': state_id}
    order_serializer = OrderSerializer(data=order_data)
    if order_serializer.is_valid():
        order = order_serializer.save()

        # Add the cart items to the order
        for cart_item in cart_items:
            cart_item_data = {'fk_id_order': order.id, 'fk_id_product': cart_item.fk_id_product, 'quantity': cart_item.quantity, 'price': cart_item.total_price}
            cart_item_serializer = CartItemSerializer(data=cart_item_data)
            if cart_item_serializer.is_valid():
                cart_item_serializer.save()

        # Clear the user's cart
        cart_items.delete()

        return Response(order_serializer.data, status=201)
    return Response(order_serializer.errors, status=400)


# @api_view(['GET'])
# def list_products_order(request):
#     orderItem_data = Order_items.objects.prefetch_related('fk_id_order__fk_id_state', 'fk_id_user__fk_id_people', 'fk_id_order__fk_id_product').all()
        
#     if orderItem_data:
#         orderItem_serializer = OrderItemSerializer(orderItem_data, many= True)
#         response_data = []
        
#         for orderItem_obj in orderItem_serializer.data:
#             state_id = orderItem_obj['fk_id_state']
#             state_obj = States.objects.get(pk=state_id)
#             orderItem_obj['state_data'] = {'id': state_id, 'name': state_obj.name}
            
#             products_id = orderItem_obj['fk_id_product']
#             product_obj = Products.objects.get(pk=products_id)
#             orderItem_obj['product_data'] = {'id': products_id, 'name': product_obj.name}
            
#             user_id = orderItem_obj['fk_id_user']
#             user_obj = Users.objects.get(pk=Peoples.name)
#             orderItem_obj['user_data'] = {'id': user_id, 'name': user_obj.fk_id_people.name}

#             order_id = orderItem_obj['fk_id_order']
#             order_obj = Orders.objects.get(pk=order_id)
#             orderItem_obj['order_data'] = {'id': order_id, 'total_price': order_obj.total_price}
            
#             # Agrega más campos relacionados según tus necesidades
            
#             orderItem_obj.pop('fk_id_state')
#             orderItem_obj.pop('fk_id_product')
#             orderItem_obj.pop('fk_id_user')
#             orderItem_obj.pop('fk_id_order')
            
#             response_data.append(orderItem_obj)
