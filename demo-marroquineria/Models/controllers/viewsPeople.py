from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_people(request):
    queryset = People.objects.all()
    serializer = PeopleSerializer(queryset, many=True)

    if not serializer.data:
        response_data = {
            'code': 'HTTP_404_NOT_FOUND',
            'message': 'No encontrado',
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

@api_view(['POST'])
def create_people(request):
    serializer = PeopleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Verificar si la persona ya existe
    name = serializer.validated_data['name']
    existing_person = People.objects.filter(name=name).first()
    if existing_person:
        return Response(data={'code': 'HTTP_400_BAD_REQUEST', 'message': 'La persona ya existe', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data={'code': 'HTTP_201_CREATED', 'message': 'Creado Exitosamente', 'status': True}, status=status.HTTP_201_CREATED)
     

@api_view(['PATCH'])
def update_people(request, pk):
    try:
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response(data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = PeopleSerializer(people, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Actualizado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_people(request, pk):
    try:
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response (data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    people.delete()
    return Response (data={'code':'HTTP_202_ACCEPTED', 'message':'Eliminado Exitosamente', 'status':True}, status=status.HTTP_202_ACCEPTED)

