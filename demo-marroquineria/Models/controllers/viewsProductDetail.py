from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailProds
from ..serializers import *
import requests

# @api_view(['POST'])
# def product_create(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         product = serializer.save()
#         detail_data = request.data.get('detailprods')
#         if detail_data:
#             detail_serializer = DetailProdSerializer(data=detail_data)
#             if detail_serializer.is_valid():
#                 detail_serializer.save(fk_id_product=product)
#             else:
#                 return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def product_create(request):
    reference = request.data.get('reference')
    name = request.data.get('name')
    
    # Verificar si ya existe un producto con la misma referencia
    existing_product_by_reference = Products.objects.filter(reference=reference).exists()
    if existing_product_by_reference:
        return Response({"error": f"A product with reference '{reference}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Verificar si ya existe un producto con el mismo nombre
    existing_product_by_name = Products.objects.filter(name=name).exists()
    if existing_product_by_name:
        return Response({"error": f"A product with the name '{name}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()

        detail_data = request.data.get('detailprods')
        if detail_data:
            # Verificar si ya existe un detalle de producto para el producto creado
            existing_detail = DetailProds.objects.filter(fk_id_product=product).exists()
            if existing_detail:
                return Response({"error": "A detail for this product already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            detail_data['fk_id_product'] = product.id
            detail_serializer = DetailProdSerializer(data=detail_data)
            if detail_serializer.is_valid():
                detail_serializer.save()
            else:
                return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Product and detail created successfully."},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def edit_product(request, pk): # FUNCIONA
    try:
        product = Products.objects.get(id=pk)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        
        if product_serializer.is_valid():
            product = product_serializer.save()
        else:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'Error en los datos del producto', 
                                  'status': False,
                                  'data': product_serializer.errors})

        detail_data = request.data.get('detailprods')
        if detail_data:
            detail_prods = DetailProds.objects.filter(fk_id_product=product)
            for detail_instance, detail_info in zip(detail_prods, detail_data):
                detail_serializer = DetailProdSerializer(detail_instance, data=detail_info, partial=True)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    return Response(data={'code': status.HTTP_200_OK, 
                                          'message': 'Error en los datos del detalle del producto', 
                                          'status': False,
                                          'data': detail_serializer.errors})

        # Serializar los detalles y agregarlos a los datos de respuesta
        detail_prods = DetailProds.objects.filter(fk_id_product=product)
        detail_serializer = DetailProdSerializer(detail_prods, many=True)
        product_data = product_serializer.data
        product_data['detailprods'] = detail_serializer.data

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Consulta Realizada Exitosamente', 
                              'status': True,
                              'data': product_data})
    except Products.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Producto no encontrado', 
                              'status': False},
                        status=status.HTTP_404_NOT_FOUND)

# Listar
@api_view(['GET'])
def product_details(request):
    try:
        products = Products.objects.all()
        product_data = []  # List to store product data

        for product in products:
            product_serializer = ProductSerializer(product)
            state_obj = product.fk_id_state
            state_serializer = StateSerializer(state_obj)
            
            detail_prods = DetailProds.objects.filter(fk_id_product=product)
            detail_serializer = DetailProdSerializer(detail_prods, many=True)

            product_data.append({
                "product": product_serializer.data,
                "state": state_serializer.data,
                "details": detail_serializer.data
            })

        return Response(product_data, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({"error": "Products not found"}, status=status.HTTP_404_NOT_FOUND)

    

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
