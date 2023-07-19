import base64
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from demo_marroquineria import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def recuperar_contrasena(request):
    email = request.data.get('email')

    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        response_data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Usuario no existente',
            'status': False
        }
        return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    token = default_token_generator.make_token(user)
    uid_base64 = base64.urlsafe_b64encode(force_bytes(user.pk)).decode()
    reset_password_url = f'{settings.FRONTEND_URL}/{uid_base64}/{token}/'

    asunto = 'Recuperación de contraseña'
    mensaje = f'Estimado(a) {user.name},\n\n' \
              'Se ha solicitado una recuperación de contraseña para tu cuenta en nuestro sitio web Marquet Place.\n\n' \
              'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña:\n\n' \
              f'{reset_password_url}\n\n' \
              'Si no solicitaste esta recuperación de contraseña, puedes ignorar este correo.\n\n' \
              'Saludos,\n' \
              'Marquet Place'

    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

    return Response(
        data={
            'code': status.HTTP_200_OK,
            'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña',
            'status': True
        },
        status=status.HTTP_200_OK
    )

User = get_user_model()

@api_view(['POST'])
def cambiar_contrasena(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response(
                data={'code': 'HTTP_400_BAD_REQUEST', 
                      'message': 'Las contraseñas no coinciden', 
                      'status': False}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        subject = 'Contraseña Restablecida Exitosamente'
        message = f'Hola {user.name},\n\nTu contraseña ha sido restablecida exitosamente.\n \
        La nueva contraseña es: {new_password}\n\nSaludos,\n Marquet Place'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response(
            data={'code':'200_OK', 
                  'message': 'Contraseña restablecida exitosamente', 
                  'status':True}, 
            status=status.HTTP_200_OK
        )

    return Response(
        data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 
              'message': 'El enlace de restablecimiento de contraseña es inválido', 
              'status':False}, 
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
