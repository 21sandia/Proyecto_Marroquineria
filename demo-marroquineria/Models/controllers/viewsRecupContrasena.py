from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Users

@api_view(['POST'])
def recuperar_contrasena(request):
    data = request.data
    email = data.get('email')

    try:
        user = Users.objects.get(fk_id_people__email=email)
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
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = reverse('cambiar_contrasena') + f'?uidb64={uid}&token={token}'

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
    recipient_list = [user.fk_id_people.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.',
        'data': None
    })


#  ** Cambiar Contraseña **
@api_view(['POST'])
@authentication_classes([SessionAuthentication])  # Usar la autenticación de sesión de Django
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden acceder
def cambiar_contrasena(request):
    data = request.data
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if not new_password or not confirm_new_password:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Faltan parámetros requeridos.',
            'data': None
        })

    if new_password != confirm_new_password:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Las contraseñas no coinciden.',
            'data': None
        })

    if len(new_password) < 8:
        return Response({
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La contraseña debe tener al menos 8 caracteres.',
            'data': None
        })

    # Aquí obtén el usuario autenticado (reemplaza esta línea con la forma adecuada de obtener el usuario autenticado)
    user = request.user

    # Actualizar la contraseña del usuario
    user.set_password(new_password)
    user.save()

    return Response({
        'code': status.HTTP_200_OK,
        'status': True,
        'message': 'La contraseña se ha cambiado exitosamente.',
        'data': None
    })

