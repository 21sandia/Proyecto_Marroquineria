from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
exclude = ['groups']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])
    groups = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Group.objects.all(),
        required = False
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'last_name', 'document', 'date_birth', 
                  'phone', 'address', 'groups', 'password', 'user_rol', 'fk_id_status')
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

    
class recup_ContrasenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'reference', 'price', 'fk_id_status', 'fk_id_type_prod']

    def get_image(self, obj):
        return f"http://localhost:8000{obj.image.url}"
        

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status_g
        fields = '__all__'

class TypeProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProd
        fields = '__all__'

class DetailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProd
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSale
        fields = '__all__'

"""
class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'
"""

