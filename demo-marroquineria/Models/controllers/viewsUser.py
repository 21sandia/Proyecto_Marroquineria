from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests


def enviar_correo_confirmacion(user_name, user_email):
    # Asunto y cuerpo del correo electrónico
    asunto = 'Confirmación de registro y bienvenida'
    mensaje = f'¡Bienvenido(a) {user_name}!, \n \
    Gracias por registrarte en nuestro sitio web. Tu cuenta ha sido creada exitosamente.\n\n \
    Saludos,\n \
    MarquetPlace'
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)

# @api_view(['POST'])
# def create_user(request):
#     serializer = UserSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     validated_data = serializer.validated_data

#     if Users.objects.filter(email=validated_data['email']).exists():
#         return Response(
#             data={
#                 'code':status.HTTP_200_OK,
#                 'message':'Este usuario ya existe',
#                 'status': True
#             })

#     user_name = validated_data['name']
#     user_email = validated_data['email']
    
#     try:
#         enviar_correo_confirmacion(user_name,user_email)
#         serializer.save()

#     except requests.ConnectionError:
#         return Response(
#             data={
#                 'code': status.HTTP_503_SERVICE_UNAVAILABLE,
#                 'message': 'Error de conexión o de red',
#                 'status': False
#             })

#     except Exception:
#         return Response(
#             data={
#                 'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message': 'El servidor ha fallado',
#                 'status': False
#             })

#     return Response(data={'code': status.HTTP_200_OK, 
#                           'message': 'Creado Exitosamente', 
#                           'status': True})


@api_view(['GET'])
def list_user(request):
    queryset = Users.objects.all().order_by('name')
    serializer = UserSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {'code': status.HTTP_200_OK,
                         'message': 'No hay usuarios registrados',
                         'status': True}
        return Response(response_data)

    response_data = {'code': status.HTTP_200_OK,
                     'message': 'Consulta Realizada Exitosamente',
                     'status': True,
                     'data': serializer.data}
    return Response(response_data)


@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 
                              'message':'No Encontrado', 
                              'status':True})
    
    try:
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'code':status.HTTP_200_OK, 
                              'message':'Actualizado Exitosamente', 
                              'status':True})
    except Exception as e:
        # Any server error happened
        return Response(
            data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                  'message': f'Error del Servidor: {str(e)}',
                  'status': False})


@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message':'Usuario no encontrado', 
                              'status': False})
    
    try:
        user.delete()
    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                              'message':'Error al eliminar el usuario', 
                              'status':False})

    return Response(data={'code': status.HTTP_200_OK, 
                          'message':'Eliminado Exitosamente', 
                          'status': True})