from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Peoples
from ..serializers import *
import requests


@api_view(['GET'])
def list_people(request):
    queryset = Peoples.objects.all().order_by('name')
    serializer = PeopleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay personas registradas',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)

@api_view(['POST'])
def create_people(request):
    try:
        serializer = PeopleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        document = serializer.validated_data['document']
        
        existing_people_email = Peoples.objects.filter(email=email).first()
        existing_people_document = Peoples.objects.filter(document=document).first()

        if existing_people_email:
            return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                                  'message': 'Ya existe una persona con este email', 
                                  'status': False})
        elif existing_people_document:
            return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                                  'message': 'Ya existe una persona con este documento', 
                                  'status': False})
        else:
            serializer.save()
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'Se ha creado exitosamente', 
                                  'status': True})
    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Network Error', 
                              'status': False})
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Server Error: '+str(e), 
                              'status': False})
    
@api_view(['PATCH'])
def update_people(request, pk):
    try:
        people = Peoples.objects.get(pk=pk)

        serializer = PeopleSerializer(people, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Actualizado Exitosamente', 
                              'status': True})

    except Peoples.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor: ' + str(e), 
                              'status': False})

@api_view(['DELETE'])
def delete_people(request, pk):
    try:
        people = Peoples.objects.get(pk=pk)
        people.delete()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminado exitosamente', 
                              'status': True})

    except Peoples.DoesNotExist:
        return Response(data={'code': status.HTTP_404_NOT_FOUND, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_400_BAD_REQUEST, 
                              'message': 'Error de red', 
                              'status': False})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': False})

