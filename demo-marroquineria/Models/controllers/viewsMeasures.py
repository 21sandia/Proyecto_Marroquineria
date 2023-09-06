from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests


@api_view(['POST'])
def create_measures(request):
    try:
        serializer = MeasureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        existing_measures = Measures.objects.filter(name=name).first()
        if existing_measures:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'La medida ya existe', 
                                  'status': False,
                                  'data': [name]
                                  })

        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Creado Exitosamente', 
                              'status': True,
                              'data': [name]
                              })
    
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False
                              })
    
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: '+str(e), 
                              'status': False
                              })

    

@api_view(['GET'])
def list_measures(request):
    queryset = Measures.objects.all().order_by('id')
    serializer = MeasureSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay medidas registradas',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

    
@api_view(['PATCH'])
def update_measures(request, pk):
    try:
        measure = Measures.objects.get(pk=pk)

        serializer = MeasureSerializer(measure, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizado Exitosamente', 
                              'status': True,
                              'data': []
                              })

    except Measures.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Medidas No encontradas', 
                              'status': False,
                              'data': []
                              })

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: ' + str(e), 
                              'status': False,
                              'data': []
                              })

@api_view(['DELETE'])
def delete_measures(request, pk):
    try:
        measure = Measures.objects.get(pk=pk)
        measure.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True,
                              'data': []
                              })

    except Measures.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'Medidas No encontradas', 
                              'status': False,
                              'data': []
                              })

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False,
                              'data': []
                              })

    except Exception as e:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No se puede eliminar este dato mientras esté en uso', 
                              'status': False,
                              'data': []})


