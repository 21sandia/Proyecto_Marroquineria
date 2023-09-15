from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailProds
from ..serializers import *
import requests
from django.db import DatabaseError


@api_view(['POST'])
def product_create(request):
    alerts = []

    product_serializer = ProductSerializer(data=request.data)
    detail_serializer = DetailProdSerializer(data=request.data)

    # Validar y deserializar datos de producto
    if product_serializer.is_valid():
        # valida si un roducto ya esta existe con ese nombre
        if Products.objects.filter(name=request.data['name']).exists():
            alerts.append('Ya hay un producto con este nombre')
            return Response({
                    "code": status.HTTP_200_OK,
                    "status": False,
                    "message": "Ya hay un producto con este nombre"
                })
        
        # valida si un roducto ya esta existe con esa referencia
        if Products.objects.filter(reference=request.data['reference']).exists():
            alerts.append('Ya hay un producto con esta referencia')
            return Response({
                    "code": status.HTTP_200_OK,
                    "status": False,
                    "message": "Ya hay un producto con esta referencia"
                })
        
        product = product_serializer.save()
        # Agregar fk_id_product a la descripción
        request.data['fk_id_product'] = product.id
    else:
        return Response(product_serializer.errors, status=400)
    
    if 'image' in request.FILES:
        Products.image = request.FILES['image']

    # Validar y deserializar datos de detalle del producto
    if detail_serializer.is_valid():
        detail_serializer.save()
    else:
        # Si hay errores en la validación, eliminar el producto creado
        product.delete()
        return Response(detail_serializer.errors, status=400)

    # Comprobar si se han activado alertas
    if alerts:
        return Response({'alerts': alerts}, status=200)
    
    # Comprobar la cantidad del producto creado
    if product.quantity == 0:
        product_status = "No Disponible"
    else:
        product_status = "Disponible"

    return Response({
                    "code": status.HTTP_200_OK,
                    "status": True,
                    "message": "Producto y detalle creados exitosamente.",
                    "product_status": product_status})


@api_view(['PUT'])
def edit_product(request, product_id):
    # Inicializamos la respuesta de la API con valores predeterminados
    response = {
        "code": status.HTTP_200_OK,
        "status": True,
        "message": "No hay información disponible",
        "data": []}

    try:
        # Buscamos el producto existente en la base de datos utilizando su ID
        product = Products.objects.get(pk=product_id)
        # Buscamos el detalle del producto existente en la base de datos
        detail = DetailProds.objects.get(fk_id_product=product_id)
    except Products.DoesNotExist:
        # Si el producto no existe, devolvemos una respuesta de error 404
        response["message"] = "Producto no encontrado."
        return Response({"code": status.HTTP_200_OK,
                        "status": False,
                        "message": "Producto no encontrado.",
                        "data": []})
    except DetailProds.DoesNotExist:
        # Si el detalle del producto no existe, devolvemos una respuesta de error 404
        response["message"] = "Detalle del producto no encontrado."
        return Response({"code": status.HTTP_200_OK,
                        "status": True,
                        "message": "Detalle de Producto no encontrado.",
                        "data": []})

    # Copiamos los datos de la solicitud en una variable separada
    product_data = request.data.copy()
    # Extraemos el dato "color" de la solicitud (si existe) y lo eliminamos del diccionario de datos
    detail_data = product_data.pop("color", None)

    # Obtén el nuevo nombre del producto desde los datos de la solicitud
    new_product_name = product_data.get("name")

    # Verifica si ya existe un producto con el nuevo nombre, excluyendo el producto actual
    if Products.objects.exclude(pk=product_id).filter(name=new_product_name).exists():
        # Si existe, devolvemos una respuesta de error y un mensaje indicando que el nombre ya existe
        response["message"] = "El nombre de producto ya existe en la base de datos."
        return Response({"code": status.HTTP_200_OK,
                        "status": True,
                        "message": "¡Ya existe un producto con ese nombre!",
                        "data": []})

    # Creamos un serializador para el producto con los datos de la solicitud
    product_serializer = ProductSerializer(product, data=product_data, partial=True)
    if not product_serializer.is_valid():
        # Si los datos no son válidos, devolvemos una respuesta de error con los errores de validación
        response["message"] = "Datos inválidos para el producto."
        response["data"] = product_serializer.errors
        return Response({"code": status.HTTP_200_OK,
                        "status": True,
                        "message": "Datos inválidos para el producto.",
                        "data": []})

    if detail_data is not None:
        # Si hay datos de detalle, creamos un serializador para el detalle del producto
        detail_serializer = DetailProdSerializer(detail, data=detail_data, partial=True)
        if not detail_serializer.is_valid():
            # Si los datos de detalle no son válidos, devolvemos una respuesta de error con los errores de validación
            response["message"] = "Datos inválidos para el detalle del producto."
            response["data"] = detail_serializer.errors
            return Response({"code": status.HTTP_200_OK,
                        "status": True,
                        "message": "Datos inválidos para el detalle de producto.",
                        "data": []})
        # Guardamos los datos de detalle actualizados en la base de datos
        detail_serializer.save()

    # Guardamos los datos del producto actualizados en la base de datos
    product_serializer.save()

    # Verifica si la cantidad del producto es igual a cero
    if product.quantity == 0:
        product.available = False  # Cambia el estado del producto a no disponible
        product.save()

    # Preparamos una respuesta exitosa indicando que la operación se realizó con éxito
    response["status"] = True
    response["message"] = "Producto y detalle del producto actualizados exitosamente."
    return Response({"code": status.HTTP_200_OK,
                     "status": True,
                     "message": "Producto actualizado exitosamente.",
                     "data": [product_serializer.data]})


@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
         return Response(data={'code': status.HTTP_200_OK,
                               'message': 'No se encontró el producto',
                               'status': True,
                               'data': []})
    
    try:
        details = DetailProds.objects.filter(fk_id_product=pk)
        details.delete()
        product.delete()
    except DatabaseError:
         return Response(data={'code': status.HTTP_200_OK,
                               'message': 'No se puede eliminar el producto porque generó una venta, intenta desabilitarlo',
                               'status': True,
                               'data': []})
    
    return Response(data={'code': status.HTTP_200_OK,
                               'message': 'Producto eliminado exitosamente',
                               'status': True,
                               'data': []})


# Lista producto con detalle de producto
@api_view(['GET'])
def product_details(request):
    try:
        products = Products.objects.all().order_by('id')
        product_data = []

        for product in products:
            product_serializer = ProductSerializer(product)
            state_obj = product.fk_id_state
            state_serializer = StateSerializer(state_obj)

            detail = DetailProds.objects.get(fk_id_product=product)
            detail_serializer = DetailProdSerializer(detail)

            measures_obj = Measures.objects.get(pk=detail.fk_id_measures.id)
            materials_obj = Materials.objects.get(pk=detail.fk_id_materials.id)

            product_data.append({
                "product_id": product.id,  # Agregamos el ID del producto
                "product": product_serializer.data,
                "state_id": state_obj.id,  # Agregamos el ID del estado
                "state": state_serializer.data,
                "detail_id": detail.id,  # Agregamos el ID del detalle
                "detail": detail_serializer.data,
                "measures_id": measures_obj.id,  # Agregamos el ID de las medidas
                "measures": MeasureSerializer(measures_obj).data,
                "materials_id": materials_obj.id,  # Agregamos el ID de los materiales
                "materials": MaterialSerializer(materials_obj).data})

        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "Datos listados correctamente",
            "data": product_data})
    
    except Products.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "No hay productos registrados",
            'data': []})
    
    except DetailProds.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "No hay detalles de productos registrados",
            'data': []})
    
    except Measures.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "No hay medidas registradas",
            'data': []})
    
    except Materials.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "No hay materiales registrados",
            'data': []})