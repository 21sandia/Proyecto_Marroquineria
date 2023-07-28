from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sale, DetailSale
from ..serializers import DetailSaleSerializer

@api_view(['GET'])
def get_all_datasale(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    det_sale_data = DetailSale.objects.prefetch_related('fk_id_sale').all()

    if det_sale_data:
        # Serializar los datos
        det_sale_serializer = DetailSaleSerializer(det_sale_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for det_sale_obj in det_sale_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            sale_id = det_sale_obj['fk_id_product']
            sale_obj = Sale.objects.get(pk=sale_id)
            det_sale_obj['status_data'] = {'id': sale_id, 'name': sale_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            det_sale_obj.pop('fk_id_sale')
            response_data.append(det_sale_obj) # Agregar la sale modificada a la lista de respuesta

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
    


    
