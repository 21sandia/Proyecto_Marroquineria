from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_group(request):
    queryset = Group.objects.all()
    serializer = GroupSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': 'HTTP_404_NOT_FOUND',
            'message': 'No Disponible',
            'status': False
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    response_data = {
        'code': 'HTTP_200_OK',
        'message': 'Consulta Realizada Exitosamente',
        'status': True,
        'data': serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)