from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests.exceptions import RequestException
from ..models import TypeProds
from ..serializers import *
import requests


@api_view(['POST'])
def create_type_prod(request):
    try:
        serializer = TypeProdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar si la categoría ya existe
        name = serializer.validated_data['name']
        existing_type_prod = TypeProds.objects.filter(name=name).first()
        if existing_type_prod:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'El tipo de producto Ya existe', 
                                  'status': True})

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Se ha creado exitosamente', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})


# ** Lista los datos de categoría y Tipo de producto en un solo EndPoint **
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
                    'status': True,
                    'message': 'No hay información disponible',
                    'data': []}

        return Response(response)

# ** Lista solo el tipo de producto **   
@api_view(['GET'])
def list_type_prod(request):
    queryset = TypeProds.objects.all().order_by('id')
    serializer = TypeProdSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay productos registrados',
                         'status': True}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)


@api_view(['PATCH'])
def update_type_prod(request, pk):
    try:
        type_prod = TypeProds.objects.get(pk=pk)

        # Obtén el nombre enviado en los datos del request
        name = request.data.get('name')

        # Verifica si el nuevo nombre ya existe en la base de datos, excluyendo la categoría actual
        if name != type_prod.name:
            exist_type_prod = TypeProds.objects.filter(name=name).first()
            if exist_type_prod:
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'message': 'El nombre de este tipo de producto ya existe',
                        'status': True,
                        'data': None})

        serializer = TypeProdSerializer(type_prod, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizado exitosamente', 
                              'status': True})

    except TypeProds.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})
    

@api_view(['DELETE'])
def delete_type_prod(request, pk):
    try:
        type_prod = TypeProds.objects.get(pk=pk)
        type_prod.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True})

    except TypeProds.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se encontró', 
                              'status': True})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se puede eliminar este dato mientras esté en uso', 
                              'status': False})
    
    
