<<<<<<< HEAD
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http.response import JsonResponse
from django.contrib.auth.hashers import check_password
=======
from django.http.response import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from rest_framework_simplejwt.exceptions import TokenError
>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET', 'POST', 'DELETE'])
def rol_list(request):

    if request.method == 'POST':
        rol_data = JSONParser().parse(request)
        rol_serializer = RolSerializer(data=rol_data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return JsonResponse(rol_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(rol_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

<<<<<<< HEAD
=======

>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
# ** login **

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'El email y la contraseña son requeridos',
            'data': None
        })

    try:
        user = Users.objects.get(fk_id_people__email=email)
    except Users.DoesNotExist:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Usuario no encontrado',
            'status': False
        })

    if not check_password(password, user.password):
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Contraseña incorrecta',
            'status': False
        })

<<<<<<< HEAD
    if user.fk_id_state.name == 'Activo':
        rol = user.fk_id_rol.name

        if rol in ['Administrador', 'Vendedor', 'Repartidor', 'Cliente']:
=======
    # Verificar si el usuario está autenticado
    if user.fk_id_state.name:
        # Obtener el objeto del rol del usuario
        rol = user.fk_id_rol

        if rol.name in ['Administrador', 'Empleado', 'Proveedor', 'Cliente']:
            # Generar los tokens de acceso y de actualización
>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'code': status.HTTP_200_OK,
                'access_token': access_token,
                'refresh_token': str(refresh),
                'rol_nombre': rol.name,  # Nombre del rol
                'user_id': user.id,        # ID del usuario
                'message': f'Inicio de sesión exitoso con el Rol {rol.name}',
                'status': True
            })

    return Response({
        'code': status.HTTP_200_OK,
        'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
        'status': False
    })


<<<<<<< HEAD
# @api_view(['POST'])
# def iniciar_sesion(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     # Verificar que los campos no estén vacíos
#     if not email or not password:
#         return Response({
#             'code': status.HTTP_200_OK,
#             'status': False,
#             'message': 'El email y la contraseña son requeridos',
#             'data': None
#         })

#     # Obtener el usuario a través del email
#     try:
#         user = Users.objects.get(fk_id_people__email=email)
#     except Users.DoesNotExist:
#         return Response({
#             'code': status.HTTP_200_OK,
#             'message': 'Usuario no encontrado',
#             'status': False
#         })

#     # Verificar la contraseña
#     if not check_password(password, user.password):
#         return Response({
#             'code': status.HTTP_200_OK,
#             'message': 'Contraseña incorrecta',
#             'status': False
#         })

#     # Verificar si el usuario está autenticado
#     if user.fk_id_state.name:
#         # Obtener el nombre del rol del usuario
#         rol = user.fk_id_rol.name

#         if rol in ['Administrador', 'Vendedor', 'Repartidor', 'Cliente']:
#             # Generar los tokens de acceso y de actualización
#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token

#             return Response({
#                 'code': status.HTTP_200_OK,
#                 'access_token': str(access_token),
#                 'refresh_token': str(refresh),
#                 'message': f'Inicio de sesión exitoso con el Rol {rol}',
#                 'status': True
#             })

#     # Credenciales inválidas o usuario no autenticado o rol no permitido
#     return Response({
#         'code': status.HTTP_200_OK,
#         'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
#         'status': False
#     })



=======
>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
# **CERRAR SESION**
@api_view(['POST'])
def log_out(request):
    try:
        # Intenta realizar la operación de cierre de sesión
        logout(request)
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Cierre de sesión exitoso',
            'status': True
        })
    except TokenError as e:
        # Maneja la excepción TokenError cuando el token ha expirado
        return Response({
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'El token de acceso ha expirado',
            'status': False
        })



