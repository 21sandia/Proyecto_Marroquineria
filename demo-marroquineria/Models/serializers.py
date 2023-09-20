from rest_framework import serializers
from .models import Users, Peoples, Rol, Measures, Materials, DetailProds, DetailSales, Sales, States, Products, TypeProds, Categorys, Carts, Cart_items, Orders, Order_items


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
    image = serializers.ImageField(use_url=True, required=False, default='/media/null.jpg')

    class Meta:
        model = Products
        fields = ['id', 'name', 'reference', 'image', 'description', 'quantity', 'price_shop', 'price_sale', 'fk_id_state', 'fk_id_type_prod']

    def create(self, validated_data):
        #Si 'image' no está presente en los datos validados, establece su valor como None
        if 'image' not in validated_data:
            validated_data['image'] = None

        return super().create(validated_data)
    

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measures
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'

    
class DetailProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProds
        fields = ['id','date','fk_id_product', 'color', 'fk_id_measures', 'fk_id_materials']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    fk_id_people = serializers.PrimaryKeyRelatedField(queryset=Peoples.objects.all(), allow_null=True)
    class Meta:
        model = Sales
        fields = '__all__'
        
class DetailSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSales
        fields = '__all__'



