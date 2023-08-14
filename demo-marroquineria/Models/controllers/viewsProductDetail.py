from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailProds
from ..serializers import *
import requests


@api_view(['POST'])
def product_create(request):
    # Initialize empty alerts list
    alerts = []

    product_serializer = ProductSerializer(data=request.data)
    detail_serializer = DetailProdSerializer(data=request.data)

    # Validar y deserializar datos de producto
    if product_serializer.is_valid():
        # Check if product with the same name already exists
        if Products.objects.filter(name=request.data['name']).exists():
            alerts.append('A product with the same name already exists')
            return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Ya hay un producto con este nombre"
                })
        
        # Check if product with the same reference already exists
        if Products.objects.filter(reference=request.data['reference']).exists():
            alerts.append('A product with the same reference already exists')
            return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Ya hay un producto con esta referencia"
                })
        
        product = product_serializer.save()
        # Agregar fk_id_product a la descripción
        request.data['fk_id_product'] = product.id
    else:
        return Response(product_serializer.errors, status=400)

    # Validar y deserializar datos de detalle del producto
    if detail_serializer.is_valid():
        detail_serializer.save()
    else:
        # Si hay errores en la validación, eliminar el producto creado
        product.delete()
        return Response(detail_serializer.errors, status=400)

    # Check if any alerts were triggered
    if alerts:
        return Response({'alerts': alerts}, status=200)

    return Response({
                    "code": status.HTTP_201_CREATED,
                    "status": True,
                    "message": "Producto y detalle creados exitosamente."
                })



@api_view(['PATCH'])
def edit_product(request, product_id):
    # Inicializamos una lista vacía de alertas
    alerts = []

    try:
        product = Products.objects.get(pk=product_id)
        detail = DetailProds.objects.get(fk_id_product=product_id)
    except Products.DoesNotExist:
        return Response({"message": "Producto no encontrado."}, status=404)
    except DetailProds.DoesNotExist:
        return Response({"message": "Detalle del producto no encontrado."}, status=404)

    product_data = request.data.copy()
    detail_data = request.data.copy()

    product_data.pop('fk_id_product', None)  # Eliminar fk_id_product del diccionario
    detail_data.pop('fk_id_product', None)  # Eliminar fk_id_product del diccionario

    product_serializer = ProductSerializer(product, data=product_data, partial=True)
    detail_serializer = DetailProdSerializer(detail, data=detail_data, partial=True)

    if product_serializer.is_valid() and detail_serializer.is_valid():
        if 'name' in product_data and Products.objects.filter(name=product_data['name']).exclude(pk=product_id).exists():
            alerts.append('Ya existe un producto con el mismo nombre.')
            return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Ya hay un producto con este nombre"
                })

        if 'reference' in product_data and Products.objects.filter(reference=product_data['reference']).exclude(pk=product_id).exists():
            alerts.append('Ya existe un producto con la misma referencia.')
            return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Ya hay un producto con esta referencia"
                })

        product_serializer.save()
        detail_serializer.save()

        return Response({
                    "code": status.HTTP_201_CREATED,
                    "status": True,
                    "message": "Producto actualizado exitosamente."
                })
    else:
        alerts.extend(product_serializer.errors)
        alerts.extend(detail_serializer.errors)
        return Response(alerts, status=400)
    


# @api_view(['PATCH']) 
# def edit_product(request, pk):  
#     try:
#         # Intenta obtener el objeto de producto con el ID proporcionado
#         product = Products.objects.get(id=pk)
        
#         # Crea un serializador para el producto con los datos de la solicitud (parciales)
#         product_serializer = ProductSerializer(product, data=request.data, partial=True)
        
#         if product_serializer.is_valid():  # Verifica si los datos son válidos
#             product = product_serializer.save()  # Guarda los datos actualizados del producto
#         else:
#             # Si los datos no son válidos, devuelve una respuesta de error con detalles de validación
#             return Response(data={'code': status.HTTP_200_OK, 
#                                   'message': 'Error en los datos del producto', 
#                                   'status': False,
#                                   'data': product_serializer.errors})

#         # Intenta obtener los datos de detalle del producto de la solicitud
#         detail_data = request.data.get('detailprods')
#         if detail_data:
#             # Obtiene las instancias de detalle del producto relacionadas con el producto actual
#             detail_prods = DetailProds.objects.filter(fk_id_product=product)
#             for detail_instance, detail_info in zip(detail_prods, detail_data):
#                 # Crea un serializador para cada instancia de detalle y guarda los datos actualizados
#                 detail_serializer = DetailProdSerializer(detail_instance, data=detail_info, partial=True)
#                 if detail_serializer.is_valid():
#                     detail_serializer.save()
#                 else:
#                     # Si los datos del detalle no son válidos, devuelve una respuesta de error
#                     return Response(data={'code': status.HTTP_200_OK, 
#                                           'message': 'Error en los datos del detalle del producto', 
#                                           'status': False,
#                                           'data': detail_serializer.errors})

#         # Obtiene nuevamente las instancias de detalle del producto actualizadas
#         detail_prods = DetailProds.objects.filter(fk_id_product=product)
#         detail_serializer = DetailProdSerializer(detail_prods, many=True)
#         product_data = product_serializer.data  # Obtiene los datos serializados del producto
#         product_data['detailprods'] = detail_serializer.data  # Agrega los detalles al diccionario de datos

#         # Devuelve una respuesta exitosa con los datos del producto y sus detalles
#         return Response(data={'code': status.HTTP_200_OK, 
#                               'message': 'Producto editado Exitosamente', 
#                               'status': True,
#                               'data': product_data})
#     except Products.DoesNotExist:
#         # Si no se encuentra el producto, devuelve una respuesta de error 404
#         return Response(data={'code': status.HTTP_200_OK, 
#                               'message': 'Producto no encontrado', 
#                               'status': False},
#                         status=status.HTTP_404_NOT_FOUND)


# Listar
@api_view(['GET'])  
def product_details(request):  
    try:
        products = Products.objects.all()  # Obtiene todos los objetos de productos de la base de datos
        product_data = []  # Lista para almacenar los datos de los productos y sus detalles

        for product in products:  # Itera a través de los objetos de productos
            product_serializer = ProductSerializer(product)  # Crea un serializador para el producto
            state_obj = product.fk_id_state  # Obtiene el objeto de estado asociado al producto
            state_serializer = StateSerializer(state_obj)  # Crea un serializador para el estado
            
            detail_prods = DetailProds.objects.filter(fk_id_product=product)  # Obtiene detalles del producto
            detail_serializer = DetailProdSerializer(detail_prods, many=True)  # Serializa los detalles

            # Agrega los datos serializados del producto, estado y detalles a la lista
            product_data.append({
                "product": product_serializer.data,
                "state": state_serializer.data,
                "details": detail_serializer.data
            })

        return Response(product_data, status=status.HTTP_200_OK)  # Devuelve la lista de datos de productos
    except Products.DoesNotExist:  # Manejo de excepción si no se encuentran productos
        return Response({"error": "Productos no encontrados"}, status=status.HTTP_404_NOT_FOUND)


    

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Products.objects.get(pk=pk)
        product.delete()
        # Eliminar el detalle del producto asociado
        try:
            product_detail = DetailProds.objects.get(fk_id_product=pk)
            product_detail.delete()
        except DetailProds.DoesNotExist:
            pass  # No se encontró el detalle del producto, no es necesario eliminarlo

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Producto y su detalle eliminados exitosamente', 
                              'status': True})

    except Products.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se encontró el producto', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})


