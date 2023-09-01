from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import *
from .serializers import *
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def rol_list(request):

    if request.method == 'POST':
        rol_data = JSONParser().parse(request)
        rol_serializer = RoleSerializer(data=rol_data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return JsonResponse(rol_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(rol_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
<<<<<<< Updated upstream
=======


# ** login **
@api_view(['POST'])
def iniciar_sesion(request):
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

    if user.fk_id_state.name == 'Activo':
        rol = user.fk_id_rol.name

        if rol in ['Administrador', 'Empleado', 'Proveedor', 'Cliente']:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'code': status.HTTP_200_OK,
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'message': f'Inicio de sesión exitoso con el Rol {rol}',
                'status': True
            })

    return Response({
        'code': status.HTTP_200_OK,
        'message': 'Credenciales inválidas, usuario no autenticado o rol no permitido',
        'status': False
    })


# **CERRAR SESION**
@api_view(['POST'])
def cerrar_sesion(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'El token de actualización es requerido',
            'data': None
        })

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Sesión cerrada exitosamente',
            'status': True
        })
    except Exception as e:
        return Response({
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Error al cerrar la sesión',
            'status': False
        })


>>>>>>> Stashed changes
