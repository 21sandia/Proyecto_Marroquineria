from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Peoples, Users
from ..serializers import *
import requests


@api_view(['POST'])
def create_people_and_user(request):
    data = request.data
    try:
        # Crear una instancia de People
        people = Peoples.objects.create(
            email=data['email'],
            name=data['name'],
            last_name=data['last_name'],
            type_document=data['type_document'],
            document=data['document'],
            gender=data['gender'],
            date_birth=data['date_birth'],
            phone=data['phone'],
            address=data['address']
        )

        # Crear una instancia de Rol y Estado si no existen
        rol, _ = Rol.objects.get_or_create(name=data['rol_name'])
        state, _ = States.objects.get_or_create(name=data['state_name'])

        # Crear una instancia de User asociada a People, Rol y Estado
        user = Users.objects.create(
            fk_id_state=state,
            fk_id_rol=rol,
            fk_id_people=people,
            password=data['password']
        )

        # Envío de correo de confirmación y bienvenida
        subject = 'Confirmación de registro y bienvenida'
        message = f'¡Bienvenido(a) {people.name},\n \
        Gracias por registrarte en nuestro sitio web. Tu cuenta ha sido creada exitosamente.\n\n \
        Saludos,\n \
        MarquetPlace'
        from_email = 'noreply@example.com'
        recipient_list = [people.email]
        send_mail(subject, message, from_email, recipient_list)

        people_serializer = PeopleSerializer(people)  # Serializar los datos de People

        response_data ={
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'El registro se ha realizado exitosamente',
            'data': people_serializer.data  # Agregar los datos serializados a la respuesta
        }

        return Response(response_data)

    except Exception as e:
        error_data = {'error': str(e)}
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_people(request):
    people_queryset = Peoples.objects.all().order_by('id')
    people_serializer = PeopleSerializer(people_queryset, many=True)

    if not people_serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay personas registradas',
                         'status': False}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': []}

    for person_data in people_serializer.data:
        user = Users.objects.filter(fk_id_people=person_data['id']).first()
        user_data = {}

        if user:
            user_serializer = UserSerializer(user)
            user_data = user_serializer.data

            if 'fk_id_rol' in user_data:
                user_data['fk_id_rol'] = {
                    'id': user.fk_id_rol.id,
                    'name': user.fk_id_rol.name
                }

            if 'fk_id_state' in user_data:
                user_data['fk_id_state'] = {
                    'id': user.fk_id_state.id,
                    'name': user.fk_id_state.name
                }

            del user_data['fk_id_people']

        person_data['users'] = user_data
        response_data['data'].append(person_data)

    return Response(response_data)


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
    except Peoples.DoesNotExist:
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos no encontrados',
            'data': None
        }
        return Response(responde_data)
    try:
        user = Users.objects.get(fk_id_people=people)
        user.delete()
    except Users.DoesNotExist:
        pass

    people.delete()

    responde_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos eliminados exitosamente',
            'data': None
        }
    return Response(responde_data)

