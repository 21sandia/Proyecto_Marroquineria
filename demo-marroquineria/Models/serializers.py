from rest_framework import serializers
from .models import Users, Peoples, Rol, Measures, Materials, DetailProds, DetailSales, Sales, States, Products, TypeProds, Categorys, Carts, Cart_items


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ('id', 'name')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id', 'name')


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
        fields = ('id', 'name', 'last_name', 'email', 'type_document', 'document', 'gender', 'date_birth', 'phone', 'address', 'employee', 'supplier', 'customer')

    
class recup_ContrasenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        fields = '__all__'


class TypeProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProds
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'reference', 'image', 'description', 'quantity', 'price_shop', 'price_sale', 'fk_id_state', 'fk_id_type_prod']

    
class DetailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProds
        fields = ['id','date','fk_id_product', 'color', 'fk_id_measures', 'fk_id_materials']
    

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(source='fk_id_people.id', read_only=True)
    person_name = serializers.CharField(source='fk_id_people.name', read_only=True)
    person_document = serializers.IntegerField(source='fk_id_people.document', read_only=True)
    person_email = serializers.CharField(source='fk_id_people.email', read_only=True)
    state_id = serializers.IntegerField(source='fk_id_state.id', read_only=True)
    state_name = serializers.CharField(source='fk_id_state.name', read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = ['id', 'date', 'total_sale', 'person_id', 'person_name', 'person_document', 'person_email', 'state_id', 'state_name', 'products']

    def get_products(self, obj):
        products = DetailSales.objects.filter(fk_id_sale_id=obj.id).values('fk_id_prod__id', 'fk_id_prod__name', 'quantity', 'price_unit', 'total_product')
        return list(products)


class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSales
        fields = '__all__'



