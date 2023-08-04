from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
import requests


@api_view(['POST'])
def create_user(self, request, *args, **kwargs):
    validated_data = request.data

    people_id = validated_data.pop('fk_id_people')
    people = Peoples.objects.get(id=people_id)

    if Users.objects.filter(fk_id_people=people_id).exists():
        raise serializers.ValidationError('A User for this Person already exists')

    validated_data['email'] = people.email

    user = Users(fk_id_people=people, **validated_data)
    user.set_password(validated_data['password'])
    user.save()

    # Send welcome email to the user
    send_mail(
        'Bienvenido a nuestra plataforma Market Place',
        'Estimado(a) {},\n\nGracias por registrarse con nosotros. Su cuenta se ha creado correctamente'.format(people.name),
        'noreply@example.com',
        [people.email],
        fail_silently=False,)
    
    data = {}

    return Response(data)


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