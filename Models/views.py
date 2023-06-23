from rest_framework import viewsets
from .serializer import *

from .models import Role, People
from .models import Category, Type_prod, Product
from .models import Order, Carts, Detail_sale

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()  # Lista de elementos del modelo
    serializer_class = RoleSerializer

class PeopleViewSet(viewsets.ModelViewSet):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class Type_prodViewSet(viewsets.ModelViewSet):
    queryset = Type_prod.objects.all()
    serializer_class = Type_prodSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartsViewSet(viewsets.ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartsSerializer

class Detail_saleViewSet(viewsets.ModelViewSet):
    queryset = Detail_sale.objects.all()
    serializer_class = Detail_saleSerializer

    
