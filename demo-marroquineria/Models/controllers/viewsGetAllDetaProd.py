from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, DetailProd
from ..serializers import DetailProdSerializer

@api_view(['GET'])
def get_all_datap(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    det_prod_data = DetailProd.objects.prefetch_related('fk_id_sale').all()

    if det_prod_data:
        # Serializar los datos
        det_prod_serializer = DetailProdSerializer(det_prod_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for det_prod_obj in det_prod_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            product_id = det_prod_obj['fk_id_product']
            product_obj = Product.objects.get(pk=product_id)
            det_prod_obj['status_data'] = {'id': product_id, 'name': product_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            det_prod_obj.pop('fk_id_product')
            # Agregar el producto modificado a la lista de respuesta
            response_data.append(det_prod_obj)

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

    


