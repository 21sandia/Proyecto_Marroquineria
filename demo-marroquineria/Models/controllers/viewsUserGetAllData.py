from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import User, Role, Status_g
from ..serializers import RoleSerializer, StatusSerializer, UserSerializer

@api_view(['GET'])
def get_related_foreign_keys(request):
    # Obtener todos los datos de usuarios y sus datos relacionados
    user_data = User.objects.select_related('fk_id_status', 'user_rol').all()

    # Serializar los datos de usuarios
    user_serializer = UserSerializer(user_data, many=True)
    user_data = user_serializer.data

    # Obtener los roles relacionados con usuarios
    roles_data = Role.objects.filter(user__isnull=False).distinct()

    # Serializar los datos de roles
    roles_serializer = RoleSerializer(roles_data, many=True)
    roles_data = roles_serializer.data

    # Obtener los estados relacionados con usuarios
    status_data = Status_g.objects.filter(user__isnull=False).distinct()

    # Serializar los datos de estados
    status_serializer = StatusSerializer(status_data, many=True)
    status_data = status_serializer.data

    # Agregar los datos de roles y estados a cada usuario en la respuesta final
    for user_obj in user_data:
        user_obj['role_data'] = [{'id': role['id'], 'name': role['name']} for role in roles_data if role['id'] == user_obj['user_rol']]
        user_obj['status_data'] = [{'id': status['id'], 'name': status['name']} for status in status_data if status['id'] == user_obj['fk_id_status']]

    return Response(data={'code': status.HTTP_200_OK, 'message': 'Datos obtenidos Exitosamente', 'status': True, 'data': user_data})


