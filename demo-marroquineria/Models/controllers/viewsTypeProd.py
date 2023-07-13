from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_type_prod(request):
    queryset = TypeProd.objects.all()
    serializer = Type_prodSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_type_prod(request):
    serializer = Type_prodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Verificar si el tipo de producto ya existe
    name = serializer.validated_data['name']
    existing_type = TypeProd.objects.filter(name=name).first()
    if existing_type:
        return Response(data={'code': 'HTTP_400_BAD_REQUEST', 'message': 'El tipo de producto ya existe', 'status': False}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data={'code': 'HTTP_201_CREATED', 'message': 'Creado Exitosamente', 'status': True}, status=status.HTTP_201_CREATED)
      

@api_view(['PATCH'])
def update_type_prod(request, pk):
    try:
        type_prod = TypeProd.objects.get(pk=pk)
    except TypeProd.DoesNotExist:
        return Response(data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = Type_prodSerializer(type_prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'HTTP_201_CREATED', 'message':'Actualizado Exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def delete_type_prod(request, pk):
    try:
        type_prod = TypeProd.objects.get(pk=pk)
    except TypeProd.DoesNotExist:
        return Response (data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 'message':'No Encontrado', 'status':True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    type_prod.delete()
    return Response (data={'code':'HTTP_201_CREATED', 'message':'Elminado Exitosamente', 'status':True}, status=status.HTTP_204_NO_CONTENT)