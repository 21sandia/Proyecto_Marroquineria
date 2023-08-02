from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Peoples, Users, Rol, States
from ..serializers import RolSerializer, StateSerializer, UserSerializer, PeopleSerializer

@api_view(['GET'])
def get_related_foreign_keys(request):
    # obtener todos los datos del Usuario y sus datos relacionados
    user_data = Users.objects.select_related('fk_id_state', 'user_rol', 'fk_id_people').all()

    # serializa Datos de user
    user_serializer = UserSerializer(user_data, many=True)
    user_data = user_serializer.data

    # obtener Roles relacionados con User
    rol_data = Rol.objects.filter(users__isnull=False).distinct()
    # serializa Datos de Rol
    rol_serializer = RolSerializer(rol_data, many=True)
    rol_data = rol_serializer.data

    # Obtener estados relacionados con user
    states_data = States.objects.filter(users__isnull=False).distinct()
    # serializar datos de Estados
    states_serializer = StateSerializer(states_data, many=True)
    states_data = states_serializer.data

    # obtener todos los datos de las personas relacionados con los usuarios
    peoples_data = Peoples.objects.filter(users__isnull=False).distinct()
    # serializar los datos de Peoples
    peoples_serializer = PeopleSerializer(peoples_data, many=True)
    peoples_data = peoples_serializer.data

    # añadir datos de Roles, Estados y peoples a cada Usuario en la respuesta final
    for user_obj in user_data:
        user_obj['rol_data'] = [{'id': rol['id'], 'name': rol['name']} for rol in rol_data if rol['id'] == user_obj['fk_id_rol']]
        user_obj['states_data'] = [{'id': states['id'], 'name': states['name']} for states in states_data if states['id'] == user_obj['fk_id_state']]      
        user_obj['peoples_data'] = [{'id': people['id'], 'name': people['name']} for people in peoples_data if people['id'] == user_obj['fk_id_people']]

    # eliminar los campos "fk_id_rol", "fk_id_state" y "fk_id_people" del diccionario
    user_obj.pop('fk_id_rol', None)
    user_obj.pop('fk_id_state', None)
    user_obj.pop('fk_id_people', None)

    return Response(data={'code': status.HTTP_200_OK, 'message': 'Data obtained successfully',
                          'status': True, 'data': user_data})


