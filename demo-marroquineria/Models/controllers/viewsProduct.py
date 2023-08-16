from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import *

# ** Lista los datos de estado, categoría, tipo de producto y producto en un solo EndPoint **
@api_view(['GET'])
def get_Product(request): # FUNCIONA
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
    


@api_view(['GET'])
def get_all_Product(request):
    try:
        # Obtener el parámetro de consulta "product_id" si está presente
        product_id = request.query_params.get('product_id')

        detail_prod_data = DetailProds.objects.select_related(
            'fk_id_product__fk_id_state',
            'fk_id_product__fk_id_type_prod__fk_id_category',
        ).all()

        # Si se proporciona un "product_id", aplicar el filtro por ID del producto
        if product_id:
            detail_prod_data = detail_prod_data.filter(fk_id_product_id=product_id)

        # Obtener la lista de detalles de productos resultantes
        detail_prod_data = detail_prod_data.all()

        response_data = []
        
        if detail_prod_data:
            response_data = []

            for detail_prod_obj in detail_prod_data:
                product_obj = detail_prod_obj.fk_id_product
                state_obj = product_obj.fk_id_state
                category_obj = product_obj.fk_id_type_prod.fk_id_category

                type_prod_obj = product_obj.fk_id_type_prod

                detail_data = DetailProdSerializer(detail_prod_obj).data
                product_data = {
                    'id': product_obj.id,
                    'name': product_obj.name,
                    'image_url': product_obj.image.url if product_obj.image else None,
                    'reference': product_obj.reference,
                    'description': product_obj.description,
                    'quantity': product_obj.quantity,
                    'price_shop': str(product_obj.price_shop),
                    'price_sale': str(product_obj.price_sale),
                    'state_data': {
                        'id': state_obj.id,
                        'name': state_obj.name
                    },
                    'category_data': {
                        'id': category_obj.id,
                        'name': category_obj.name
                    },
                    'type_prod_data': {
                        'id': type_prod_obj.id,
                        'name': type_prod_obj.name
                    }
                }

                detail_data['product_data'] = product_data
                response_data.append(detail_data)

            response = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Consulta realizada Exitosamente',
                'data': response_data
            }
        else:
            response = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'No hay información disponible',
                'data': []
            }

        return Response(response)
    except DetailProds.DoesNotExist:
        response = {
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'No se encontraron detalles de productos',
            'data': []
        }

        return Response(response)




