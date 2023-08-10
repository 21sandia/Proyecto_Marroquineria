from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailProds
from ..serializers import *
import requests


@api_view(['POST']) 
def product_create(request):  
    reference = request.data.get('reference')  # Obtiene el valor del campo 'reference' de la solicitud
    name = request.data.get('name')  # Obtiene el valor del campo 'name' de la solicitud
    
    # Verifica si ya existe un producto con la misma referencia en la base de datos
    existing_product_by_reference = Products.objects.filter(reference=reference).exists()
    if existing_product_by_reference:
        return Response({"code": status.HTTP_200_OK,
                         "status": False,
                         "message": f"Error: El producto con referencia '{reference}' ya existe."})

    # Verifica si ya existe un producto con el mismo nombre en la base de datos
    existing_product_by_name = Products.objects.filter(name=name).exists()
    if existing_product_by_name:
        return Response({"code": status.HTTP_200_OK,
                         "status": False,
                         "message": f"Error: El producto con nombre '{name}' ya existe."})

    # Crea una instancia del serializador ProductSerializer con los datos de la solicitud
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():  # Verifica si los datos son válidos
        product = serializer.save()  # Guarda el nuevo producto en la base de datos

        detail_data = request.data.get('detailprods')  # Obtiene los datos del detalle del producto
        if detail_data:
            # Verifica si ya existe un detalle de producto para el producto creado
            existing_detail = DetailProds.objects.filter(fk_id_product=product).exists()
            if existing_detail:
                return Response({"code": status.HTTP_200_OK,
                                 "status": False,
                                 "message": "Error: El detalle de producto para este producto ya existe."})

            detail_data['fk_id_product'] = product.id  # Asigna el ID del producto al detalle
            detail_serializer = DetailProdSerializer(data=detail_data)  # Crea un serializador para el detalle
            if detail_serializer.is_valid():
                detail_serializer.save()  # Guarda el detalle en la base de datos
            else:
                return Response({"code": status.HTTP_400_BAD_REQUEST,
                                 "status": False,
                                 "message": "Error en los datos del detalle del producto",
                                 "data": detail_serializer.errors})

        return Response({"code": status.HTTP_200_OK,
                         "status": True,
                         "message": "Producto creado exitosamente."})
    return Response({"code": status.HTTP_400_BAD_REQUEST,
                     "status": False,})





@api_view(['PATCH']) 
def edit_product(request, pk):  
    try:
        # Intenta obtener el objeto de producto con el ID proporcionado
        product = Products.objects.get(id=pk)
        
        # Crea un serializador para el producto con los datos de la solicitud (parciales)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)
        
        if product_serializer.is_valid():  # Verifica si los datos son válidos
            product = product_serializer.save()  # Guarda los datos actualizados del producto
        else:
            # Si los datos no son válidos, devuelve una respuesta de error con detalles de validación
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'Error en los datos del producto', 
                                  'status': False,
                                  'data': product_serializer.errors})

        # Intenta obtener los datos de detalle del producto de la solicitud
        detail_data = request.data.get('detailprods')
        if detail_data:
            # Obtiene las instancias de detalle del producto relacionadas con el producto actual
            detail_prods = DetailProds.objects.filter(fk_id_product=product)
            for detail_instance, detail_info in zip(detail_prods, detail_data):
                # Crea un serializador para cada instancia de detalle y guarda los datos actualizados
                detail_serializer = DetailProdSerializer(detail_instance, data=detail_info, partial=True)
                if detail_serializer.is_valid():
                    detail_serializer.save()
                else:
                    # Si los datos del detalle no son válidos, devuelve una respuesta de error
                    return Response(data={'code': status.HTTP_200_OK, 
                                          'message': 'Error en los datos del detalle del producto', 
                                          'status': False,
                                          'data': detail_serializer.errors})

        # Obtiene nuevamente las instancias de detalle del producto actualizadas
        detail_prods = DetailProds.objects.filter(fk_id_product=product)
        detail_serializer = DetailProdSerializer(detail_prods, many=True)
        product_data = product_serializer.data  # Obtiene los datos serializados del producto
        product_data['detailprods'] = detail_serializer.data  # Agrega los detalles al diccionario de datos

        # Devuelve una respuesta exitosa con los datos del producto y sus detalles
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Producto editado Exitosamente', 
                              'status': True,
                              'data': product_data})
    except Products.DoesNotExist:
        # Si no se encuentra el producto, devuelve una respuesta de error 404
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Producto no encontrado', 
                              'status': False},
                        status=status.HTTP_404_NOT_FOUND)


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


