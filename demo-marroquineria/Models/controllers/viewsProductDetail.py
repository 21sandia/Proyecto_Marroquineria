from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailProds
from ..serializers import *
import requests


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
    try:
        product = Products.objects.get(pk=product_id)
        detail = DetailProds.objects.get(fk_id_product=product_id)
    except Products.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                        "status": False,
                        "message": "Producto no encontrado",
                        'data': []
                        })
    except DetailProds.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                        "status": False,
                        "message": "Detalle de Producto no encontrado",
                        'data': []
                        })

    product_data = request.data.copy()
    detail_data = {
        "color": product_data.pop("color", ""),
        "fk_id_measures": product_data.pop("fk_id_measures"),
        "fk_id_materials": product_data.pop("fk_id_materials")
    }

    product_serializer = ProductSerializer(product, data=product_data, partial=True)
    detail_serializer = DetailProdSerializer(detail, data=detail_data, partial=True)

    if product_serializer.is_valid() and detail_serializer.is_valid():
        if 'name' in product_data and Products.objects.filter(name=product_data['name']).exclude(pk=product_id).exists():
            return Response({"code": status.HTTP_200_OK,
                            "status": False,
                            "message": "Ya existe un producto con este nombre",
                            'data': []
                            })

        if 'reference' in product_data and Products.objects.filter(reference=product_data['reference']).exclude(pk=product_id).exists():
            return Response({"code": status.HTTP_200_OK,
                            "status": False,
                            "message": "Ya existe un producto con esta referencia",
                            'data': []
                            })

        product_serializer.save()
        detail_serializer.save()

        return Response({"code": status.HTTP_200_OK,
                        "status": False,
                        "message": "Producto actualizado exitosamente",
                        'data': []
                        })
    else:
        errors = product_serializer.errors
        errors.update(detail_serializer.errors)
        return Response(errors, status=status.HTTP_200_OK)



# Lista producto con detalle de producto
@api_view(['GET'])
def product_details(request):
    try:
        products = Products.objects.all()
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
                "product": product_serializer.data,
                "state": state_serializer.data,
                "detail": detail_serializer.data,
                "measures": MeasureSerializer(measures_obj).data,
                "materials": MaterialSerializer(materials_obj).data
            })

        return Response(product_data, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                         "status": False,
                         "message": "No hay productos registrados",
                         'data': []
                         })
    
    except DetailProds.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                         "status": False,
                         "message": "No hay detalles de productos registrados",
                         'data': []
                         })
    
    except Measures.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                        "status": False,
                        "message": "No hay medidas registradas",
                        'data': []
                         })
    
    except Materials.DoesNotExist:
        return Response({"code": status.HTTP_200_OK,
                         "status": False,
                         "message": "No hay materiales registrados",
                         'data': []
                         })
    

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
                              'message': 'Producto eliminado exitosamente', 
                              'status': True,
                              'data': []
                              })

    except Products.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se encontró el producto', 
                              'status': False,
                              'data': []
                              })

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False,
                              'data': []
                              })


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





