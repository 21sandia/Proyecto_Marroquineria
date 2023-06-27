from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer


    @action(methods=['post'], detail=True)
    def product(self, request, pk):
        people = self.get_object()