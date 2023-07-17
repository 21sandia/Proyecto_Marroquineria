import base64
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import *
from rest_framework import status


@api_view(['POST'])
def recuperar_contrasena(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'No se encontró ningún usuario con este correo electrónico',
                'status': False
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # Generar un token de seguridad
    token = default_token_generator.make_token(user) # GENERA EL TOKEN
    uid_base64 = base64.urlsafe_b64encode(force_bytes(user.pk)) # GENERA EL TOKEN CIFRADO POR SEGURIDAD
    reset_link = f'{settings.FRONTEND_URL}/{uid_base64}/{token}/'  # ENDPOINT PARA RESTABLECER CONTRASEÑA

    # Asunto y cuerpo del correo electrónico
    asunto = 'Recuperación de contraseña'
    mensaje = f'Estimado(a) {user.name},\n\n' \
              'Se ha solicitado una recuperación de contraseña para tu cuenta en nuestro sitio web.\n\n' \
              'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña:\n\n' \
              f'{reset_link}\n\n' \
              'Si no solicitaste esta recuperación de contraseña, puedes ignorar este correo.\n\n' \
              'Saludos,\n' \
              'Tu aplicación'

    # Envío del correo electrónico
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

    # Enviar el correo electrónico con el enlace para restablecer la contraseña

    return Response(
        data={
            'code': status.HTTP_200_OK,
            'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña',
            'status': True
        },
        status=status.HTTP_200_OK
    )
    # Construir el enlace de recuperación de contraseña

User = get_user_model()
@api_view(['POST'])
def cambiar_contrasena(request, uid, token):
    uid_base64 = request.data.get('uid')
    token = request.data.get('token')
    password = request.data.get('password')

    if not uid_base64:
        return Response(
            data={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'El enlace de restablecimiento de contraseña es inválido',
                'status': False
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        uid = force_str(urlsafe_base64_decode(uid_base64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            data={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'El enlace de restablecimiento de contraseña es inválido',
                'status': False
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if default_token_generator.check_token(user, token):
        user.set_password(password)
        user.save()
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'La contraseña ha sido cambiada exitosamente',
                'status': True
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'El enlace de restablecimiento de contraseña es inválido',
                'status': False
            },
            status=status.HTTP_400_BAD_REQUEST
        )