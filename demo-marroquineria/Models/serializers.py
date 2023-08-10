from rest_framework import serializers
from .models import Users, Peoples, Rol, DetailProds, DetailSales, Sales, States, Products, TypeProds, Categorys

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('fk_id_state', 'fk_id_rol', 'fk_id_people', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        fk_id_people = validated_data.pop('fk_id_people')
        validated_data['is_active'] = True

        # Obtener la instancia de la persona relacionada
        people = Peoples.objects.get(id=fk_id_people)

        # Crear y guardar el nuevo usuario con la relación con la persona
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.fk_id_people = people
        user.save()

        return user


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peoples
        fields = ('id', 'name', 'last_name', 'email', 'type_document', 'document', 'gender', 'date_birth', 'phone', 'address')

    
class recup_ContrasenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(use_url=True) 

    class Meta:
        model = Products
        fields = ['id', 'name', 'reference', 'image', 'description', 'quantity', 'price_shop', 'price_sale', 'fk_id_state', 'fk_id_type_prod']

    

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ('id', 'name')

class TypeProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProds
        fields = '__all__'

class DetailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProds
        fields = ['date', 'color', 'size_p', 'material']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSales
        fields = '__all__'




