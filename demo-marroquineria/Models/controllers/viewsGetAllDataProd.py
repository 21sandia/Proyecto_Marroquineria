from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products, States, TypeProds, Categorys
from ..serializers import ProductSerializer

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
            category_id = type_prod_obj.fk_id_category
            category_obj = Categorys.objects.get(pk=category_id)
            product_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            product_obj.pop('fk_id_state')
            product_obj.pop('fk_id_type_prod')
            response_data.append(product_obj) # Agregar el producto modificado a la lista de respuesta

        response = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada Exitosamente',
            'data': response_data
        }

        # Retornar la respuesta con los datos serializados y modificados
        return Response(response)
    else:
        response = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No hay información disponible',
            'data': []
        }

        return Response(response)

