from django.contrib.auth.models import Group

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    groups = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Group.objects.all(),
        required = False
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'last_name', 'document', 'date_birth', 'phone', 'address', 'is_staff', 'is_active', 'groups', 'password', 'user_rol', 'fk_id_status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        groups_data = validate_data.pop('groups', [])
        password = validate_data.pop('password')
        validate_data['is_active'] = True
        user = self.Meta.model(**validate_data)
        user.set_password(password)
        user.save()

        if groups_data:
            user.user_rol.groups.set(groups_data)

        return user
        
    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups',  None)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
            user.save()

        if groups_data:
            Role.groups.set(groups_data)
        
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
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

