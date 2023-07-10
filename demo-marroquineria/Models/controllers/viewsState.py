from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_state(request):
    queryset = State.objects.all()
    serializer = StateSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_state(request):
    serializer = StateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Creado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_state(request, pk):
    try:
        state = State.objects.get(pk=pk)
    except State.DoesNotExist:
        return Response(data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = StateSerializer(state, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Actualizado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_state(request, pk):
    try:
        state = State.objects.get(pk=pk)
    except State.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    state.delete()
    return Response (data={'code':'HTTP_201_CONTENT', 'message':'Eliminado Exitosamente', 'status':True}, status=status.HTTP_204_NO_CONTENT)