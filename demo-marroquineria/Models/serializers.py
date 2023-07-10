from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        return get_user_model().objects.create_user(**validate_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save
        
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class Type_prodSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProd
        fields = '__all__'

class Detail_prodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProd
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class Detail_saleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSale
        fields = '__all__'

"""
class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'
"""

