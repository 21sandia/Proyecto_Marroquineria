from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from .models import *
from .serializers import *
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def rol_list(request):

    if request.method == 'POST':
        rol_data = JSONParser().parse(request)
        rol_serializer = RoleSerializer(data=rol_data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return JsonResponse(rol_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(rol_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
