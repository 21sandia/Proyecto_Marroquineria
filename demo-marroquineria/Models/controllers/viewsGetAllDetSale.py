from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sale, DetailSale
from ..serializers import DetailSaleSerializer

@api_view(['GET'])
def get_all_datasale(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    det_sale_data = DetailSale.objects.prefetch_related('fk_id_sale').all()

    # Serializar los datos
    det_sale_serializer = DetailSaleSerializer(det_sale_data, many=True)

    # Modificar los datos para agregar los nombres del producto
    response_data = []
    for det_sale_obj in det_sale_serializer.data:
        # Obtener el ID del producto y el nombre asociado
        sale_id = det_sale_obj['fk_id_product']
        sale_obj = Sale.objects.get(pk=sale_id)
        det_sale_obj['status_data'] = {'id': sale_id, 'name': det_sale_obj.name}

        # Eliminar los campos de las claves foráneas que ya no se necesitan
        det_sale_obj.pop('fk_id_sale')

        # Agregar el producto modificado a la lista de respuesta
        response_data.append(det_sale_obj)

    # Retornar la respuesta con los datos serializados y modificados
    response = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Datos obtenidos Exitosamente',
        'data': response_data
    }

    return Response(response)