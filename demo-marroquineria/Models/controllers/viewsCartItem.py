from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models import Carts, Cart_items, Products
from ..serializers import *

from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.request import Request


@api_view(['POST'])
def add_to_cart(request: Request):
    # Obtener el ID del usuario del cuerpo del request
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'code': status.HTTP_200_OK, 
                         'message': 'ID de usuario no proporcionado',
                         'status': True})

    # Buscar el usuario por su ID o devolver un error si no existe
    user = get_object_or_404(Users, pk=user_id)

    # Obtener el ID del producto y la cantidad del cuerpo del request
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    # Obtener el producto y verificar si hay suficiente stock
    try:
        product = Products.objects.get(pk=product_id)
    except Products.DoesNotExist:
        return Response({'code': status.HTTP_400_BAD_REQUEST,
                         'message': 'Producto no encontrado',
                         'status': False})
    
    if product.quantity == 0 or product.quantity < quantity:
        # Si la cantidad en stock es igual a cero o menor que la cantidad solicitada, devuelve un mensaje de error
        return Response({'code': status.HTTP_400_BAD_REQUEST,
                         'message': 'No hay suficiente stock disponible',
                         'status': False})

    # Calcular el precio total
    total_price = product.price_sale * int(quantity)

    # Verificar si el usuario tiene un carrito existente
    try:
        cart = Carts.objects.get(fk_id_user=user)
    except Carts.DoesNotExist:
        # Si el usuario no tiene un carrito, crea uno
        cart = Carts.objects.create(fk_id_user=user)

    # Verificar si el producto ya está en el carrito del usuario
    try:
        cart_item = Cart_items.objects.get(fk_id_cart=cart, fk_id_product=product)
        # Si el producto ya está en el carrito, actualiza la cantidad y el precio total
        cart_item.quantity += int(quantity)
        cart_item.total_price += total_price
        cart_item.save()
    except Cart_items.DoesNotExist:
        # Si el producto no está en el carrito, crea un nuevo elemento en el carrito
        Cart_items.objects.create(fk_id_cart=cart, fk_id_product=product, quantity=quantity, total_price=total_price)

    return Response({'code': status.HTTP_200_OK,
                     'message': 'Producto añadido al carrito con éxito',
                     'status': True})


#Quitar un producto del carrito
@api_view(['POST'])
def remove_product_from_cart(request):
    # Obtener el ID del usuario del cuerpo del request
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'ID de usuario no proporcionado',
                         'status': True})

    # Buscar el usuario por su ID o devolver un error si no existe
    user = get_object_or_404(Users, pk=user_id)

    # Obtener el ID del producto del cuerpo del request
    product_id = request.data.get('product_id')

    # Verificar si el usuario tiene un carrito existente
    try:
        cart = Carts.objects.get(fk_id_user=user)
    except Carts.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'error': 'El usuario no tiene un carrito',
                         'status': True})

    # Verificar si el producto está en el carrito del usuario y eliminarlo si es necesario
    try:
        cart_item = Cart_items.objects.get(fk_id_cart=cart, fk_id_product=product_id)
        cart_item.delete()  # Eliminar el producto del carrito
        return Response({'code': status.HTTP_200_OK,
                         'message': 'Producto eliminado del carrito con éxito',
                         'status': True})
    except Cart_items.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'El producto no está en el carrito',
                         'status': True})


#Disminuir la cantidad de un producto en el carrito 
@api_view(['POST'])
def decrease_product_quantity(request):
    # Obtener el ID del usuario del cuerpo del request
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'ID de usuario no proporcionado',
                         'status': True})

    # Buscar el usuario por su ID o devolver un error si no existe
    user = get_object_or_404(Users, pk=user_id)

    # Obtener el ID del producto del cuerpo del request
    product_id = request.data.get('product_id')

    # Verificar si el usuario tiene un carrito existente
    try:
        cart = Carts.objects.get(fk_id_user=user)
    except Carts.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'El usuario no tiene un carrito',
                         'status': True})

    # Verificar si el producto está en el carrito del usuario y disminuir la cantidad si es necesario
    try:
        cart_item = Cart_items.objects.get(fk_id_cart=cart, fk_id_product=product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Disminuir la cantidad en 1 unidad
            cart_item.total_price = cart_item.quantity * cart_item.fk_id_product.price_sale  # Actualizar el precio total
            cart_item.save()
        else:
            cart_item.delete()  # Si la cantidad es 1, eliminar el producto del carrito
        return Response({'code': status.HTTP_200_OK,
                         'message': 'Cantidad del producto disminuida con éxito',
                         'status':True})
    except Cart_items.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'El producto no está en el carrito',
                         'status': True})


@api_view(['POST'])
def clear_cart(request, user_id):
    # Buscar el usuario por su ID o devolver un error si no existe
    user = get_object_or_404(Users, pk=user_id)

    # Verificar si el usuario tiene un carrito existente
    try:
        cart = Carts.objects.get(fk_id_user=user)
    except Carts.DoesNotExist:
        return Response({'code': status.HTTP_200_OK,
                         'message': 'El usuario no tiene un carrito',
                         'status': True})

    # Eliminar todos los productos del carrito
    Cart_items.objects.filter(fk_id_cart=cart).delete()

    return Response({'code': status.HTTP_200_OK,
                     'message': 'Carrito limpiado con éxito',
                     'status': True})


@api_view(['GET'])
def list_cart(request, user_id):
    # Buscar el usuario por su ID o devolver un error si no existe
    user = get_object_or_404(Users, pk=user_id)

    # Verificar si el usuario tiene un carrito existente
    try:
        cart = Carts.objects.get(fk_id_user=user)
    except Carts.DoesNotExist:
        return Response({'error': 'El usuario no tiene un carrito'}, status=status.HTTP_404_NOT_FOUND)

    # Obtener los elementos del carrito del usuario
    cart_items = Cart_items.objects.filter(fk_id_cart=cart)

    # Serializar los elementos del carrito a JSON (puedes usar serializers de Django Rest Framework)
    serialized_cart_items = serialize_cart_items(cart_items)

    # Devolver la respuesta con los elementos del carrito
    return Response({'cart_items': serialized_cart_items}, status=status.HTTP_200_OK)

def serialize_cart_items(cart_items):
    # Esta función debe tomar una lista de elementos del carrito y serializarlos a formato JSON.
    # Puedes utilizar serializers de Django Rest Framework o crear un diccionario manualmente.

    serialized_items = []

    for item in cart_items:
        serialized_item = {
            'product_id': item.fk_id_product.id,
            'product_name': item.fk_id_product.name,
            'quantity': item.quantity,
            'total_price': str(item.total_price),
        }
        serialized_items.append(serialized_item)

    return serialized_items





