from rest_framework import serializers
from .models import Users, Peoples, Rol, DetailProds, DetailSales, Sales, States, Products, TypeProds, Categorys


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = Users
        fields = ('fk_id_state', 'fk_id_rol', 'fk_id_people', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        password = validate_data.pop('password')
        validate_data['is_active'] = True
        user = self.Meta.model(**validate_data)
        user.set_password(password)
        user.save()

        return user


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peoples
        fields = '__all__'

    
class recup_ContrasenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True) 

    class Meta:
        model = Products
        fields = ['id', 'name', 'image', 'reference', 'description', 'quantity', 'price_shop', 'price_sale', 'fk_id_state', 'fk_id_type_prod']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__'

class TypeProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProds
        fields = '__all__'

class DetailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProds
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSales
        fields = '__all__'




