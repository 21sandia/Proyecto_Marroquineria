from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import TypeProds, Categorys
from ..serializers import TypeProdSerializer

@api_view(['GET'])
def get_all_tpcateg(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    type_prod_data = TypeProds.objects.prefetch_related('fk_id_category').all()

    if type_prod_data:
        # Serializar los datos
        type_prod_serializer = TypeProdSerializer(type_prod_data, many=True)
        response_data = []

        # Modificar los datos para agregar el tipo de producto y categoría
        for type_prod_obj in type_prod_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            category_id = type_prod_obj['fk_id_category']
            category_obj = Categorys.objects.get(pk=category_id)
            type_prod_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            type_prod_obj.pop('fk_id_category')
            response_data.append(type_prod_obj) # Agregar el producto modificado a la lista de respuesta


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
    


    
