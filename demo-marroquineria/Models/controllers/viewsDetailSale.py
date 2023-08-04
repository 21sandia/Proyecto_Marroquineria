from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import DetailSales
from ..serializers import *


@api_view(['POST'])
def create_detail_sale(request):
    data = request.data

    existing_details = []
    for detail_data in data:
        existing_detail = DetailSales.objects.filter(**detail_data).first()
        if existing_detail:
            existing_details.append(existing_detail)

    if existing_details:
        serializer = DetailSaleSerializer(existing_details, many=True)
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Algunos objetos ya existen.', 
                              'status': False, 
                              'data': serializer.data})

    serializer = DetailSaleSerializer(data=data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 
                          'message': 'Creado Exitosamente', 
                          'status': True, 
                          'data': serializer.data})


# ** Lista los datos de detalle venta con venta en un EndPoint **
@api_view(['GET'])
def get_all_datasale(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    det_sale_data = DetailSales.objects.prefetch_related('fk_id_sale').all()

    if det_sale_data:
        # Serializar los datos
        det_sale_serializer = DetailSaleSerializer(det_sale_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for det_sale_obj in det_sale_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            sale_id = det_sale_obj['fk_id_sale']
            sale_obj = Sales.objects.get(pk=sale_id)
            det_sale_obj['sale_data'] = {'id': sale_id, 'name': sale_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            det_sale_obj.pop('fk_id_sale')
            response_data.append(det_sale_obj) # Agregar la venta modificada a la lista de respuesta

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
def update_detail_sale(request, pk):
    try:
        detail_sale = DetailSales.objects.get(pk=pk)
    except DetailSales.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No Encontrado', 
                              'status': True})
    
    serializer = DetailSaleSerializer(detail_sale, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code': status.HTTP_200_OK, 
                          'message': 'Actualizado Exitosamente', 
                          'status': True})

@api_view(['DELETE'])
def delete_detail_sale(request, pk):
    try:
        detail_sale = DetailSales.objects.get(pk=pk)
    except DetailSales.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No Encontrado', 
                              'status': True})
    
    detail_sale.delete()
    return Response(data={'code': status.HTTP_200_OK, 
                          'message': 'Eliminado Exitosamente', 
                          'status': True})
