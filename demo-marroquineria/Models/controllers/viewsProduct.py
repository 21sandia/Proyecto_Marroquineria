from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import *
import requests


@api_view(['POST'])
def create_product(request):
    try:
        # Verificar si el producto ya existe
        name = request.data.get('name', None)
        existing_product = Products.objects.filter(name=name).first()
        if existing_product:
            return Response(data={
                'code': status.HTTP_200_OK, 
                'message': 'El producto ya existe', 
                'status': False
            })

        # Crear el serializer y realizar la validación de precios
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        price_shop = serializer.validated_data.get('price_shop')
        price_sale = serializer.validated_data.get('price_sale')

        if price_shop is not None and price_sale is not None and price_sale < price_shop:
            return Response(data={'code': status.HTTP_200_OK,
                                  'message': "El precio de venta debe ser mayor o igual al precio de compra.",
                                  'status': False,
                                  'errors': serializer.errors})

        # Agregar el código para enviar la imagen
        image = request.FILES.get('image')
        if image:
            serializer.validated_data['image'] = image

        # Guardar el producto en la base de datos
        serializer.save()

        return Response(data={
            'code': status.HTTP_200_OK,
            'message': 'Producto creado exitosamente', 
            'status': True
        })

    except requests.ConnectionError:
        return Response(data={
            'code': status.HTTP_400_BAD_REQUEST, 
            'message': 'Error de red', 
            'status': False
        })

    except Exception as e:
        return Response(data={
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
            'message': 'Error del servidor', 
            'status': False
        })


@api_view(['GET'])
def list_product(request):
    queryset = Products.objects.all().order_by('name')
    serializer = ProductSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay productos registrados',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)


# ** Lista los datos de estado, categoría, tipo de producto y producto en un solo EndPoint **
@api_view(['GET'])
def get_all_models_data(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    product_data = Products.objects.prefetch_related('fk_id_state', 'fk_id_type_prod__fk_id_category').all()

    if product_data:
        # Serializar los datos
        product_serializer = ProductSerializer(product_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for product_obj in product_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            state_id = product_obj['fk_id_state']
            state_obj = States.objects.get(pk=state_id)
            product_obj['state_data'] = {'id': state_id, 'name': state_obj.name}

            # Obtener el ID del tipo de producto y el nombre asociado
            type_prod_id = product_obj['fk_id_type_prod']
            type_prod_obj = TypeProds.objects.get(pk=type_prod_id)
            product_obj['type_prod_data'] = {'id': type_prod_id, 'name': type_prod_obj.name}

            # Obtener el ID de la categoría y el nombre asociado
            category_id = type_prod_obj.fk_id_category_id
            category_obj = Categorys.objects.get(pk=category_id)
            product_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            product_obj.pop('fk_id_state')
            product_obj.pop('fk_id_type_prod')
            response_data.append(product_obj) # Agregar el producto modificado a la lista de respuesta

        response = {'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'Consulta realizada Exitosamente',
                    'data': response_data}

        # Retornar la respuesta con los datos serializados y modificados
        return Response(response)
    else:
        response = {'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'No hay información disponible',
                    'data': []}

        return Response(response)
    

# ** Lista los datos de todo el producto en un solo EndPoint **
@api_view(['GET'])
def get_all_models_prod_detailp(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    product_data = Products.objects.prefetch_related('fk_id_state', 'fk_id_type_prod__fk_id_category','detailprods_set').all()

    if product_data:
        # Serializar los datos
        product_serializer = ProductSerializer(product_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for product_obj in product_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            state_id = product_obj['fk_id_state']
            state_obj = States.objects.get(pk=state_id)
            product_obj['state_data'] = {'id': state_id, 'name': state_obj.name}

            # Obtener el ID del tipo de producto y el nombre asociado
            type_prod_id = product_obj['fk_id_type_prod']
            type_prod_obj = TypeProds.objects.get(pk=type_prod_id)
            product_obj['type_prod_data'] = {'id': type_prod_id, 'name': type_prod_obj.name}

            # Obtener el ID de la categoría y el nombre asociado
            category_id = type_prod_obj.fk_id_category_id
            category_obj = Categorys.objects.get(pk=category_id)
            product_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Obtener el ID de detalle producto y el nombre asociado
            detail_prod_id = product_obj['detailprods_set']
            detail_prod_obj = DetailProds.objects.get(pk=detail_prod_id)
            product_obj['detail_prod_data'] = {'id': detail_prod_id, '': detail_prod_obj}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            product_obj.pop('fk_id_state')
            product_obj.pop('fk_id_type_prod')
            product_obj.pop('detailprods_set')
            response_data.append(product_obj) # Agregar el producto modificado a la lista de respuesta

        response = {'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'Consulta realizada Exitosamente',
                    'data': response_data}

        # Retornar la respuesta con los datos serializados y modificados
        return Response(response)
    else:
        response = {'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'No hay información disponible',
                    'data': []}

        return Response(response)


@api_view(['PATCH'])
def update_product(request, pk):
    try:
        product = Products.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        # Comprueba si hay un archivo de imagen en la solicitud
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': status.HTTP_200_OK,
                         'message': 'Actualizado exitosamente', 
                         'status': True
        })
    except Products.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Products.objects.get(pk=pk)
        product.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True})

    except Products.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})
