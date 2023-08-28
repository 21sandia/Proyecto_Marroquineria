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
            alerts.append('A product with the same name already exists')
            return Response({
                    "code": status.HTTP_404_NOT_FOUND,
                    "status": False,
                    "message": "Ya hay un producto con este nombre"
                })
        
        # valida si un roducto ya esta existe con esa referencia
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
    
    if 'image' in request.FILES:
        Products.image = request.FILES['image']

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


@api_view(['PUT'])
def edit_product(request, product_id):
    response = {
        "code": status.HTTP_200_OK,
        "status": False,
        "message": "No hay información disponible",
        "data": []
    }

    try:
        product = Products.objects.get(pk=product_id)
        detail = DetailProds.objects.get(fk_id_product=product_id)
    except Products.DoesNotExist:
        response["message"] = "Producto no encontrado."
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except DetailProds.DoesNotExist:
        response["message"] = "Detalle del producto no encontrado."
        return Response(response, status=status.HTTP_404_NOT_FOUND)

    product_data = request.data.copy()
    detail_data = product_data.pop("color", None)

    product_serializer = ProductSerializer(product, data=product_data, partial=True)
    if not product_serializer.is_valid():
        response["message"] = "Datos inválidos para el producto."
        response["data"] = product_serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    if detail_data is not None:
        detail_serializer = DetailProdSerializer(detail, data=detail_data, partial=True)
        if not detail_serializer.is_valid():
            response["message"] = "Datos inválidos para el detalle del producto."
            response["data"] = detail_serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        detail_serializer.save()

    product_serializer.save()

    response["status"] = True
    response["message"] = "Producto y detalle del producto actualizados exitosamente."
    return Response(response, status=status.HTTP_200_OK)





@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
         return Response(data={'code': status.HTTP_404_NOT_FOUND,
                               'message': 'No se encontró el producto',
                               'status': False,
                               'data': []
                               })
    
    try:
        details = DetailProds.objects.filter(fk_id_product=pk)
        details.delete()
        product.delete()
    except DatabaseError:
         return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                               'message': 'No se puede eliminar el producto porque generó una venta, intenta desabilitarlo',
                               'status': False,
                               'data': []
                              })
    
    return Response(data={'code': status.HTTP_200_OK,
                               'message': 'Producto eliminado exitosamente',
                               'status': True,
                               'data': []
                               })





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
                "materials": MaterialSerializer(materials_obj).data
            })

        return Response({
            "code": status.HTTP_200_OK,
            "status": True,
            "message": "Datos listados correctamente",
            "data": product_data
        }, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": False,
            "message": "No hay productos registrados",
            'data': []
        })
    except DetailProds.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": False,
            "message": "No hay detalles de productos registrados",
            'data': []
        })
    except Measures.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": False,
            "message": "No hay medidas registradas",
            'data': []
        })
    except Materials.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "status": False,
            "message": "No hay materiales registrados",
            'data': []
        })




