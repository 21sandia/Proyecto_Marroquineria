import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

def enviar_correo_confirmacion(user_name, user_email):
    # Asunto y cuerpo del correo electrónico
    asunto = 'Confirmación de registro y bienvenida'
    mensaje = f'¡Bienvenido(a) {user_name}!, \n \
    Gracias por registrarte en nuestro sitio web. Tu cuenta ha sido creada exitosamente.\n\n \
    Saludos,\n \
    MarquetPlace'
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    if User.objects.filter(email=validated_data['email']).exists():
        return Response(
            data={
                'code':status.HTTP_200_OK,
                'message':'Este usuario ya existe',
                'status': True
            })

    user_name = validated_data['name']
    user_email = validated_data['email']
    enviar_correo_confirmacion(user_name,user_email)
    serializer.save()

    # Envío del correo de confirmación
    

    return Response(data={'code': status.HTTP_200_OK, 'message': 'Creado Exitosamente', 'status': True})


@api_view(['GET'])
def list_user(request):
    queryset = User.objects.all().order_by('name')
    serializer = UserSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay usuarios registrados',
            'status': True
        }
        return Response(response_data)

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Consulta Realizada Exitosamente',
        'status': True,
        'data': serializer.data
    }
    return Response(response_data)

@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 'message':'No Encontrado', 'status':True})
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':status.HTTP_200_OK, 'message':'Actualizado Exitosamente', 'status':True})

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 'message':'No Encontrado', 'status':True})
    
    user.delete()
    return Response(data={'code':status.HTTP_200_OK, 'message':'Elminado Exitosamente', 'status':True})