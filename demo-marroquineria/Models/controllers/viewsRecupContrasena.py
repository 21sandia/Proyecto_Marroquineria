import base64
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
<<<<<<< HEAD
from rest_framework.response import Response
from rest_framework import status
from ..models import Users
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
=======
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ..models import *

>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7

@api_view(['POST'])
def recover_password(request):
    # Obtener el correo electrónico del usuario desde la solicitud POST
    email = request.data.get('email')

<<<<<<< HEAD
    # Verificar si el correo electrónico es válido
    try:
        validate_email(email)
    except ValidationError:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'El correo electrónico proporcionado no es válido.',
            'data': None
        })

    try:
        user = Users.objects.get(fk_id_people__email=email)
    except Users.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'No se encontró un usuario con este correo electrónico.',
            'data': None
        })
=======
    # Buscar un usuario en la base de datos con el correo electrónico proporcionado
    user = Users.objects.filter(fk_id_people__email=email).first()
    
    # Si no se encuentra un usuario con ese correo electrónico, responder con un mensaje de error
    if not user:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'No se encontró ningún usuario con este correo electrónico',
                'status': False
            })
>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7

    # Generar un token de seguridad para el usuario
    token = default_token_generator.make_token(user)
    timezone.now()  # Esto parece ser un código innecesario, ya que no se está utilizando.
    
    # Codificar el ID del usuario y el token en base64 para formar un enlace de restablecimiento
    uid_base64 = base64.urlsafe_b64encode(force_bytes(user.pk)).decode()
    reset_link = f'{settings.FRONTEND_URL}/{uid_base64}/{token}/'

<<<<<<< HEAD
    # Crear enlace para restablecer la contraseña
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(reverse('cambiar_contrasena')) + f'?uidb64={uid}&token={token}'

    # Envío de correo para recuperación de contraseña
    subject = 'Recuperación de contraseña'
    message = f'Hola {user.fk_id_people.name},\n \
    Has solicitado restablecer tu contraseña en nuestro sitio web. \
    Para continuar, por favor haz clic en el siguiente enlace:\n\n \
    {reset_url}\n\n \
    Si no has solicitado esto, puedes ignorar este correo.\n\n \
    Saludos,\n \
    MarquetPlace'
    from_email = 'ecommerce.marquetp@gmail.com'
    recipient_list = [user.fk_id_people.email]
    send_mail(subject, message, from_email, recipient_list)
=======
    # Definir el asunto y el cuerpo del correo electrónico
    asunto = 'Recuperación de contraseña'
    mensaje = f'Estimado(a) {user.fk_id_people.name},\n\n' \
              'Se ha solicitado una recuperación de contraseña para tu cuenta en nuestro sitio web.\n\n' \
              'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña:\n\n' \
              f'{reset_link}\n\n' \
              'Si no solicitaste esta recuperación de contraseña, puedes ignorar este correo.\n\n' \
              'Saludos,\n' \
              'Tu aplicación Marquet Place'

    # Enviar el correo electrónico de recuperación de contraseña
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [user.fk_id_people.email], fail_silently=False)
>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7

    # Responder con un mensaje de éxito
    return Response(
        data={
            'code': status.HTTP_200_OK,
            'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.',
            'status': True
        })

<<<<<<< HEAD
=======

>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
@api_view(['POST'])
def change_password(request, uidb64, token):
    try:
        # Decodificar el valor de uidb64 de base64 para obtener el ID del usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        
        # Buscar al usuario en la base de datos utilizando el ID obtenido
        user = Users.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
        # Si ocurre alguna excepción durante la búsqueda, establecer user como None
        user = None

<<<<<<< HEAD
    if not new_password or not confirm_new_password:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Faltan parámetros requeridos.',
            'data': None
        })

    if new_password != confirm_new_password:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Las contraseñas no coinciden.',
            'data': None
        })

    if len(new_password) < 8 or not any(char.isdigit() for char in new_password) or not any(char.isalpha() for char in new_password):
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La contraseña debe tener al menos 8 caracteres, un número y una letra.',
            'data': None
        })

    user = request.user
=======
    # Verificar si el usuario no es None y si el token es válido
    if user is not None and default_token_generator.check_token(user, token):
        # Obtener las contraseñas nuevas y confirmadas de la solicitud POST
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Verificar si las contraseñas nuevas y confirmadas coinciden
        if new_password != confirm_password:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Las contraseñas no coinciden',
                    'status': False
                })

        # Establecer la nueva contraseña para el usuario y guardar los cambios
        user.set_password(new_password)
        user.save()

        # Preparar un mensaje de éxito para el usuario
        subject = 'Contraseña Restablecida Exitosamente'
        message = f'Hola {user.fk_id_people.name},\n\nTu contraseña ha sido restablecida exitosamente.\n' 

        # Configurar el remitente y la lista de destinatarios del correo electrónico
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.fk_id_people.email]
        
        # Enviar el correo electrónico informando al usuario que su contraseña ha sido cambiada
        send_mail(subject, message, from_email, recipient_list)

        # Responder con un mensaje de éxito
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'La contraseña ha sido cambiada exitosamente',
                'status': True
            }) 
    else:
        # Si el usuario es None o el token no es válido, responder con un mensaje de error
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'El enlace de restablecimiento de contraseña es inválido',
                'status': False
            })

>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7


<<<<<<< HEAD
    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'La contraseña se ha cambiado exitosamente.',
        'data': None
    })
=======

>>>>>>> 185c76a2020d13d14e0616e166da2f447f00c1f7
