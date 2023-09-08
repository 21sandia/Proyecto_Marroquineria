from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models import *
from ..serializers import *

# Crear un carrito
@api_view(['POST'])
def create_cart(request):
    # Obtener el usuario asociado al carrito
    user_id = request.data.get('fk_id_user')

    try:
        # Verificar si el usuario existe
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Usuario no encontrado.",
            "status": False
        })

    # Crear un nuevo carrito
    cart_data = {
        'fk_id_user': user,
    }
    cart_serializer = CartSerializer(data=cart_data)
    if cart_serializer.is_valid():
        cart = cart_serializer.save()
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Carrito creado exitosamente.",
            "status": True,
            "data": cart_serializer.data
        })
    else:
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Añadir un producto al carrito
@api_view(['POST'])
def add_to_cart(request):
    # Obtener los datos de la solicitud
    cart_id = request.data.get('fk_id_cart')
    product_id = request.data.get('fk_id_product')
    quantity = request.data.get('quantity', 1)

    try:
        # Verificar si el carrito y el producto existen
        cart = Cart.objects.get(id=cart_id)
        product = Products.objects.get(id=product_id)
    except (Cart.DoesNotExist, Products.DoesNotExist):
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Carrito o producto no encontrado.",
            "status": False
        })

    # Verificar si ya existe un elemento del producto en el carrito
    try:
        cart_item = CartItem.objects.get(fk_id_cart=cart, fk_id_product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except ObjectDoesNotExist:
        # Si no existe, crear un nuevo elemento de carrito
        cart_item_data = {
            'fk_id_cart': cart,
            'fk_id_product': product,
            'quantity': quantity,
            'price': product.price_sale,  
        }
        cart_item_serializer = CartItemSerializer(data=cart_item_data)
        if cart_item_serializer.is_valid():
            cart_item_serializer.save()
        else:
            return Response(cart_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "code": status.HTTP_200_OK,
        "message": "Producto añadido al carrito exitosamente.",
        "status": True
    })

# Ver el contenido del carrito
@api_view(['GET'])
def list_cart(request, cart_id):
    try:
        # Obtener el carrito y sus elementos asociados
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(fk_id_cart=cart)
    except Cart.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Carrito no encontrado.",
            "status": False
        })

    cart_serializer = CartSerializer(cart)
    cart_item_serializer = CartItemSerializer(cart_items, many=True)

    return Response({
        "code": status.HTTP_200_OK,
        "message": "Carrito y elementos del carrito recuperados exitosamente.",
        "status": True,
        "data": {
            "cart": cart_serializer.data,
            "cart_items": cart_item_serializer.data
        }
    })

# Eliminar un producto del carrito
@api_view(['DELETE'])
def delete_cart(request, cart_id, cart_item_id):
    try:
        # Obtener el elemento del carrito y eliminarlo
        cart_item = CartItem.objects.get(fk_id_cart=cart_id, id=cart_item_id)
        cart_item.delete()
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Producto eliminado del carrito exitosamente.",
            "status": True
        })
    except CartItem.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Elemento del carrito no encontrado.",
            "status": False
        })
