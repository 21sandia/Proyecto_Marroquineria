from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Status_g, TypeProd, Category
from ..serializers import ProductSerializer

@api_view(['GET'])
def get_all_models_data(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    product_data = Product.objects.prefetch_related('fk_id_status', 'fk_id_type_prod__fk_id_category').all()

    if product_data:
        # Serializar los datos
        product_serializer = ProductSerializer(product_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for product_obj in product_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            status_id = product_obj['fk_id_status']
            status_obj = Status_g.objects.get(pk=status_id)
            product_obj['status_data'] = {'id': status_id, 'name': status_obj.name}

            # Obtener el ID del tipo de producto y el nombre asociado
            type_prod_id = product_obj['fk_id_type_prod']
            type_prod_obj = TypeProd.objects.get(pk=type_prod_id)
            product_obj['type_prod_data'] = {'id': type_prod_id, 'name': type_prod_obj.name}

            # Obtener el ID de la categoría y el nombre asociado
            category_id = type_prod_obj.fk_id_category_id
            category_obj = Category.objects.get(pk=category_id)
            product_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            product_obj.pop('fk_id_status')
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

