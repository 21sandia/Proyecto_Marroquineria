from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Peoples, Users
from ..serializers import *
import requests


@api_view(['POST'])
def create_people_and_user(request):
    data = request.data

        # Verificar si ya existe una persona con el mismo documento o correo electrónico
    existing_person_document = Peoples.objects.filter(document=data['document']).first()
    if existing_person_document:
        response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Ya existe una persona registrada con este numero de documento',
                'data': None
                }
        return Response(data=response_data)

    # Verificar si la clave 'email' está presente en los datos
    if 'email' in data:
        existing_person_email = Peoples.objects.filter(email=data['email']).first()
        if existing_person_email:
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Ya existe una persona registrada con este correo',
                'data': None
            }
            return Response(data=response_data) 
    
        # Crear una instancia de People
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
        address=data['address'],
        is_empleado=data.get('is_empleado', False),
        is_cliente=data.get('is_cliente', False)
    )

    # Crear una instancia de User asociada a People, Rol y Estado si es empleado
    if people.is_empleado:
        rol, _ = Rol.objects.get_or_create(name='Empleado')
        state = States.objects.get(pk=3)  # ID del estado activo

        hashed_password = str(people.document)  # Usar el número de documento como contraseña
        user = Users.objects.create(
            fk_id_state=state,
            fk_id_rol=rol,
            fk_id_people=people,
            password=make_password(hashed_password)
        )

    # Asignar estado y rol si es cliente
    if people.is_cliente:
        state = States.objects.get(pk=4)  # ID del estado inactivo
        rol, _ = Rol.objects.get_or_create(name='Cliente')

        people.fk_id_state = state  # Asignar estado inactivo
        people.save()  # Guardar cambios en People

        # Crear una instancia de User asociada a People, Rol y Estado
        hashed_password = str(data['document'])  # Contraseña igual al número de documento
        user = Users.objects.create(
            fk_id_state=state,
            fk_id_rol=rol,
            fk_id_people=people,
            password=make_password(hashed_password)
        )
    else:
        user = None  # No se crea usuario ni se asignan roles si no es cliente

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

        new_document = request.data.get('document', people.document)
        new_email = request.data.get('email', people.email)

        # Verificar si ya existe una persona con el mismo documento o correo electrónico
        existing_person_document = Peoples.objects.exclude(pk=pk).filter(document=new_document).first()
        if existing_person_document:
            return Response(data={'code': status.HTTP_400_BAD_REQUEST,
                                  'message': 'Ya existe una persona registrada con este número de documento',
                                  'status': False})

        existing_person_email = Peoples.objects.exclude(pk=pk).filter(email=new_email).first()
        if existing_person_email:
            return Response(data={'code': status.HTTP_400_BAD_REQUEST,
                                  'message': 'Ya existe una persona registrada con este correo electrónico',
                                  'status': False})

        # Extraer los valores actuales de is_empleado e is_cliente
        is_empleado = request.data.get('is_empleado', people.is_empleado)
        is_cliente = request.data.get('is_cliente', people.is_cliente)

        # Actualizar estado y rol si es cliente o empleado
        state = States.objects.get(pk=4)  # Estado inactivo por defecto
        rol_name = 'Cliente'  # Rol cliente por defecto

        if is_empleado:
            state = States.objects.get(pk=3)  # Estado activo para empleado
            rol_name = 'Empleado'  # Rol empleado

        if is_cliente:
            state = States.objects.get(pk=4)  # Estado inactivo para cliente

        rol, _ = Rol.objects.get_or_create(name=rol_name)

        people.fk_id_state = state
        people.is_empleado = is_empleado
        people.is_cliente = is_cliente
        people.save()

        user = Users.objects.filter(fk_id_people=people).first()
        if user:
            user.fk_id_state = state
            user.fk_id_rol = rol
            user.save()

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

