from rest_framework import serializers
from .models import Role, People
from .models import Category, Type_prod, Product
from .models import Order, Carts, Detail_sale

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class  Meta:
        model = Category
        fields = '__all__'

class Type_prodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_prod
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'

class Detail_saleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail_sale
        fields = '__all__'
