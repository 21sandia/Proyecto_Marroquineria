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



@api_view(['PUT', 'PATCH'])
def edit_product(request, product_id):
    try:
        # Obtener el producto a editar
        product = Products.objects.get(pk=product_id)

        # Validar si ya existe un producto con el mismo nombre (excepto si es el mismo producto)
        if 'name' in request.data and request.data['name'] != product.name:
            if Products.objects.filter(name=request.data['name']).exclude(pk=product_id).exists():
                return Response({
                    "code": status.HTTP_200_OK,
                    "status": False,
                    "message": "Ya existe un producto con este nombre.",
                })

        # Validar si ya existe un producto con la misma referencia (excepto si es el mismo producto)
        if 'reference' in request.data and request.data['reference'] != product.reference:
            if Products.objects.filter(reference=request.data['reference']).exclude(pk=product_id).exists():
                return Response({
                    "code": status.HTTP_200_OK,
                    "status": False,
                    "message": "Ya existe un producto con esta referencia.",
                })

        # Actualizar campos del producto
        product.name = request.data.get("name", product.name)
        product.reference = request.data.get("reference", product.reference)
        product.image = request.data.get("image", product.image)
        product.description = request.data.get("description", product.description)
        product.quantity = request.data.get("quantity", product.quantity)
        product.price_shop = request.data.get("price_shop", product.price_shop)
        product.price_sale = request.data.get("price_sale", product.price_sale)
        product.fk_id_state_id = request.data.get("fk_id_state", product.fk_id_state_id)
        product.fk_id_type_prod_id = request.data.get("fk_id_type_prod", product.fk_id_type_prod_id)
        
        # Guardar cambios en el producto
        product.save()

        # Obtener el detalle del producto relacionado
        detail, created = DetailProds.objects.get_or_create(fk_id_product=product)
        
        # Actualizar campos del detalle del producto
        detail.date = request.data.get("date", detail.date)
        detail.color = request.data.get("color", detail.color)
        detail.fk_id_measures_id = request.data.get("fk_id_measures", detail.fk_id_measures_id)
        detail.fk_id_materials_id = request.data.get("fk_id_materials", detail.fk_id_materials_id)
        
        # Guardar cambios en el detalle del producto
        detail.save()

        # Verifica si la cantidad del producto es igual a cero
        if product.quantity == 0:
            product.available = False  # Cambia el estado del producto a no disponible
            product.save()

        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "Producto y detalles actualizados exitosamente.",
        })
    except Products.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": False,
            "message": "Producto no encontrado.",
        })
    except Exception as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "status": False,
            "message": str(e),
        })


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