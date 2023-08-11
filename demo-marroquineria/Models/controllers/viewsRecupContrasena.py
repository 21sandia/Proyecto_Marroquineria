from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Users


User = get_user_model()

@api_view(['POST'])
def recuperar_contrasena(request):
    email = request.data.get('email')

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'No se encontró un usuario con este correo electrónico.',
            'data': None
        })

    # Generar token de recuperación de contraseña
    token = default_token_generator.make_token(user)

    # Crear enlace para restablecer la contraseña
    uid = urlsafe_base64_encode(force_bytes(user.id))
    reset_url = reverse('reset-password', kwargs={'uidb64': uid, 'token': token})

    # Envío de correo para recuperación de contraseña
    subject = 'Recuperación de contraseña'
    message = f'Hola {user.fk_id_people.name},\n \
        Has solicitado restablecer tu contraseña en nuestro sitio web. \
        Para continuar, por favor haz clic en el siguiente enlace:\n\n \
        {reset_url}\n\n \
        Si no has solicitado esto, puedes ignorar este correo.\n\n \
        Saludos,\n \
        MarquetPlace'
    from_email = 'noreply@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.',
        'data': None
    })


@api_view(['POST'])
def change_password(request):
    data = request.data
    uidb64 = data.get('uidb64')
    token = data.get('token')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if not uidb64 or not token or not new_password or not confirm_new_password:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Faltan parámetros requeridos.',
            'data': None
        })

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, OverflowError):
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'No se encontró un usuario válido.',
            'data': None
        })

    if not default_token_generator.check_token(user, token):
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Token no válido.',
            'data': None
        })

    if new_password != confirm_new_password:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Las contraseñas no coinciden.',
            'data': None
        })

    if len(new_password) < 8:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La contraseña debe tener al menos 8 caracteres.',
            'data': None
        })

    user.password = make_password(new_password)
    user.save()

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'La contraseña se ha cambiado exitosamente.',
        'data': None
    })
    

