from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Peoples, Users, Carts
from ..serializers import *
import requests

# @api_view(['GET'])
# def obtener_employee(request):
#     # Obtener empleados según el estado proporcionado
#     if estado == 'activo':
#         estado = States.objects.get(pk=2)  # ID del estado activo
#     elif estado == 'inactivo':
#         estado = States.objects.get(pk=3)  # ID del estado inactivo
#     else:
#         return []

#     employees = Peoples.objects.filter(employee=True, fk_id_state=estado)

#     return employees

# @api_view(['GET'])
# def obtener_supplier(estado):
#     # Obtener proveedores según el estado proporcionado
#     if estado == 'activo':
#         estado = States.objects.get(pk=2)  # ID del estado activo
#     elif estado == 'inactivo':
#         estado = States.objects.get(pk=3)  # ID del estado inactivo
#     else:
#         return []

#     suppliers = Peoples.objects.filter(supplier=True, fk_id_state=estado)

#     return suppliers

# @api_view(['GET'])
# def obtener_customer(request, estado):
#     # Obtener clientes según el estado proporcionado
#     if estado == 'activo':
#         estado = States.objects.get(pk=2)  # ID del estado activo
#     elif estado == 'inactivo':
#         estado = States.objects.get(pk=3)  # ID del estado inactivo
#     else:
#         return []

#     customers = Peoples.objects.filter(customer=True, fk_id_state=estado)

#     return customers


@api_view(['POST'])
def create_people_and_user(request):
    data = request.data

    # Verificar si la contraseña está presente en los datos
    if 'password' not in data or not data['password']:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La contraseña es requerida.',
            'data': None
        }
        return Response(data=response_data)

    # Verificar si ya existe una persona con el mismo documento o correo electrónico
    existing_person_document = Peoples.objects.filter(document=data['document']).first()
    if existing_person_document:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Ya existe una persona registrada con este número de documento',
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

    # Validar longitud y formato del número de documento
    if len(data['document']) > 10 or data['document'].startswith("0"):
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'El número de documento no es válido.',
            'data': None
        }
        return Response(data=response_data)

    # Crear una instancia de People
    people = Peoples.objects.create(
        email=data['email'],
        name=data['name'],
        last_name=data['last_name'],
        type_document=data.get('type_document', None),
        document=data['document'],
        gender=data.get('gender', None),
        date_birth=data.get('date_birth', None),
        phone=data['phone'],
        address=data.get('address', None),
        employee=data.get('employee', False),
        supplier=data.get('supplier', False),
        customer=data.get('customer', False)
    )

    # Obtener la contraseña manualmente del campo 'password' en los datos
    password = data['password']

    # Crear una instancia de User asociada a People, Rol y Estado si es empleado
    if people.employee:
        rol, _ = Rol.objects.get_or_create(name='Empleado')
        state, _ = States.objects.get_or_create(name='Activo')  # ID del estado activo
    elif people.supplier:
        rol, _ = Rol.objects.get_or_create(name='Proveedor')
        state, _ = States.objects.get_or_create(name='Activo')   # ID del estado activo
    elif people.customer:
        rol, _ = Rol.objects.get_or_create(name='Cliente')
        state, _ = States.objects.get_or_create(name='Activo')   # ID del estado activo
    # Si ninguno de los roles está configurado como True, no se asigna un rol ni un estado
    else:
        rol = None
        state = None

    user = Users.objects.create(
        fk_id_state=state,
        fk_id_rol=rol,
        fk_id_people=people,
        password=make_password(password)
    )

    # Crear un carrito para el usuario
    carts, _ = Carts.objects.get_or_create(fk_id_user=user)
    user.carts = carts
    carts.save()

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

    response_data = {
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'El registro se ha realizado exitosamente',
        'data': people_serializer.data  # Agregar los datos serializados a la respuesta
    }
    return Response(response_data)


@api_view(['GET'])
def list_people(request):
    filters = {}
    query_params = [
        'document',
        'email',
        'phone',
        'rol',
        'state'
    ]

    rol_id = request.query_params.get('rol')
    estado_id = request.query_params.get('state')

    if rol_id:
        try:
            rol_id = int(rol_id)
        except ValueError:
            # Si no es un número, intenta buscar el ID por el nombre del rol
            rol = Rol.objects.filter(name=rol_id).first()
            if rol:
                rol_id = rol.id
            else:
                # Si no se encontró el rol, no se aplica el filtro
                rol_id = None

        if rol_id is not None:
            filters['users__fk_id_rol'] = rol_id

    if estado_id:
        filters['users__fk_id_state'] = estado_id

    for param in query_params:
        value = request.query_params.get(param)
        if value and param not in ['rol', 'state']:
            filters[f'{param}__icontains'] = value

    people_queryset = Peoples.objects.filter(**filters).order_by('id')
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
                    'id': user.fk_id_rol.id if user.fk_id_rol else None,
                    'name': user.fk_id_rol.name if user.fk_id_rol else None
                }

            if 'fk_id_state' in user_data:
                user_data['fk_id_state'] = {
                    'id': user.fk_id_state.id if user.fk_id_state else None,
                    'name': user.fk_id_state.name if user.fk_id_state else None
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
            return Response(data={'code': status.HTTP_200_OK,
                                  'message': 'Ya existe una persona registrada con este número de documento',
                                  'status': False})

        existing_person_email = Peoples.objects.exclude(pk=pk).filter(email=new_email).first()
        if existing_person_email:
            return Response(data={'code': status.HTTP_200_OK,
                                  'message': 'Ya existe una persona registrada con este correo electrónico',
                                  'status': False})

        # Extraer los valores actuales de empleado, cliente y proveedor
        employee = request.data.get('employee', people.employee)
        customer = request.data.get('customer', people.customer)
        supplier = request.data.get('supplier', people.supplier)

        # Actualizar estado y rol según el estado de empleado, cliente y proveedor
        state = States.objects.get(pk=3)  # Estado inactivo por defecto
        rol_name = 'Customer'  # Rol cliente por defecto

        if employee:
            state = States.objects.get(pk=2)  # Estado activo para empleado
            rol_name = 'Employee'  # Rol empleado

        if supplier:
            state = States.objects.get(pk=2)  # Estado activo para proveedor
            rol_name = 'Supplier'  # Rol proveedor

        if customer:
            state = States.objects.get(pk=3)  # Estado inactivo para cliente

        rol, _ = Rol.objects.get_or_create(name=rol_name)

        people.fk_id_state = state
        people.employee = employee
        people.customer = customer
        people.supplier = supplier  # Actualizar proveedor
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
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': False})

    except requests.ConnectionError:
        return Response(data={'code': status.HTTP_200_OK, 
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