from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


@api_view(['GET'])
def list_role(request):
    queryset = Role.objects.all()
    serializer = RoleSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = RoleSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    role.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_people(request):
    queryset = People.objects.all()
    serializer = PeopleSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_people(request):
    serializer = PeopleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_people(request, pk):
    try:
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = PeopleSerializer(people, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_people(request, pk):
    try:
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    people.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_category(request):
    queryset = Category.objects.all()
    serializer = CategorySerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    category.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_type_prod(request):
    queryset = Type_prod.objects.all()
    serializer = Type_prodSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_type_prod(request):
    serializer = Type_prodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_type_prod(request, pk):
    try:
        type_prod = Type_prod.objects.get(pk=pk)
    except Type_prod.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = Type_prodSerializer(type_prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_type_prod(request, pk):
    try:
        type_prod = Type_prod.objects.get(pk=pk)
    except Type_prod.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    type_prod.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_product(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_order(request):
    queryset = Order.objects.all()
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    order.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_carts(request):
    queryset = Carts.objects.all()
    serializer = CartsSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_carts(request):
    serializer = CartsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_carts(request, pk):
    try:
        carts = Carts.objects.get(pk=pk)
    except Carts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = CartsSerializer(carts, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_carts(request, pk):
    try:
        carts = Carts.objects.get(pk=pk)
    except Carts.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    carts.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def list_detail_sale(request):
    queryset = Detail_sale.objects.all()
    serializer = Detail_saleSerializer(queryset, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def create_detail_sale(request):
    serializer = Detail_saleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)      

@api_view(['PATCH'])
def update_detail_sale(request, pk):
    try:
        detail_sale = Detail_sale.objects.get(pk=pk)
    except Detail_sale.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = Detail_saleSerializer(detail_sale, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_detail_sale(request, pk):
    try:
        detail_sale = Detail_sale.objects.get(pk=pk)
    except Detail_sale.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    detail_sale.delete()
    return Response (status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def list_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
