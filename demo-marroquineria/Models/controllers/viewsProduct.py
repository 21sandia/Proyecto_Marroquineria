from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import *

# ** Lista los datos de estado, categoría, tipo de producto y producto en un solo EndPoint **
@api_view(['GET'])
def get_Product(request):
    # Obtener los productos y sus foreign keys relacionadas usando prefetch_related
    product_data = Products.objects.prefetch_related('fk_id_state', 'fk_id_type_prod__fk_id_category').all()

    if product_data:
        # Serializar los datos
        product_serializer = ProductSerializer(product_data, many=True)
        response_data = []
        # Modificar los datos para agregar los nombres del estado, tipo de producto y categoría
        for product_obj in product_serializer.data:
            # Obtener el ID del estado y el nombre asociado
            state_id = product_obj['fk_id_state']
            state_obj = States.objects.get(pk=state_id)
            product_obj['state_data'] = {'id': state_id, 'name': state_obj.name}

            # Obtener el ID del tipo de producto y el nombre asociado
            type_prod_id = product_obj['fk_id_type_prod']
            type_prod_obj = TypeProds.objects.get(pk=type_prod_id)
            product_obj['type_prod_data'] = {'id': type_prod_id, 'name': type_prod_obj.name}

            # Obtener el ID de la categoría y el nombre asociado
            category_id = type_prod_obj.fk_id_category_id
            category_obj = Categorys.objects.get(pk=category_id)
            product_obj['category_data'] = {'id': category_id, 'name': category_obj.name}

            # Eliminar los campos de las claves foráneas que ya no se necesitan
            product_obj.pop('fk_id_state')
            product_obj.pop('fk_id_type_prod')
            response_data.append(product_obj) # Agregar el producto modificado a la lista de respuesta

        response = {'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'Consulta realizada Exitosamente',
                    'data': response_data}

        # Retornar la respuesta con los datos serializados y modificados
        return Response(response)
    else:
        response = {'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'No hay información disponible',
                    'data': []}

        return Response(response)


@api_view(['GET'])
def get_all_Product(request):
    data = []
    detail_prods = DetailProds.objects.all().order_by('id')

    # Obtener parámetros de filtrado y ordenación de la solicitud
    product_id = request.GET.get('product_id')
    category_id = request.GET.get('category_id')
    type_prod_id = request.GET.get('type_prod_id')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', '-date')
    name = request.GET.get('name')
    reference = request.GET.get('reference')
    state_id = request.GET.get('state_id')

    # Aplicar filtrado según ID del producto, categoría y/o tipo de producto si se proporcionan
    if product_id:
        detail_prods = detail_prods.filter(fk_id_product_id=product_id)
    if category_id:
        detail_prods = detail_prods.filter(fk_id_product__fk_id_type_prod__fk_id_category_id=category_id)
    if type_prod_id:
        detail_prods = detail_prods.filter(fk_id_product__fk_id_type_prod_id=type_prod_id)
    
    # Filtrar por rango de precio si se proporciona
    if min_price:
        detail_prods = detail_prods.filter(fk_id_product__price_sale__gte=min_price)
    if max_price:
        detail_prods = detail_prods.filter(fk_id_product__price_sale__lte=max_price)
    
    # Filtrar por nombre si se proporciona
    if name:
        detail_prods = detail_prods.filter(fk_id_product__name__icontains=name)
    
    # Filtrar por referencia si se proporciona
    if reference:
        detail_prods = detail_prods.filter(fk_id_product__reference__icontains=reference)

    # Filtrar por estado si se proporciona
    if state_id:
        detail_prods = detail_prods.filter(fk_id_product__fk_id_state_id=state_id)
    
    # Ordenar los resultados
    detail_prods = detail_prods.order_by(sort_by)

    for detail_prod in detail_prods:
        product = detail_prod.fk_id_product
        type_prod = product.fk_id_type_prod
        category = type_prod.fk_id_category
        state = product.fk_id_state
        measure = detail_prod.fk_id_measures if hasattr(detail_prod, 'fk_id_measures') else None
        material = detail_prod.fk_id_materials if hasattr(detail_prod, 'fk_id_materials') else None

        # Verificar si la cantidad es cero y mostrar el estado "no disponible"
        if product.quantity == 0:
            product_status = 0
        else:
            product_status = int(product.quantity)


        if isinstance(product.image, str):
            image_url = product.image
            image_url = "/media/" + image_url
        else:
            image_url = product.image.url if product.image else None

        data.append({
            "id": detail_prod.id,
            "date": detail_prod.date,
            "fk_id_product": product.id,
            "color": detail_prod.color,
            "product_data": {
                "id": product.id,
                "name": product.name,
                "image_url": image_url,
                "reference": product.reference,
                "description": product.description,
                "quantity": product_status,  # Mostrar estado "no disponible" si la cantidad es cero
                "price_shop": product.price_shop,
                "price_sale": product.price_sale,
                "state_data": {
                    "id": state.id,
                    "name": state.name
                },
                "category_data": {
                    "id": category.id,
                    "name": category.name
                },
                "type_prod_data": {
                    "id": type_prod.id,
                    "name": type_prod.name
                },
                "materials": {
                    "id": material.id,
                    "name": material.name
                } if material else None,
                "measures": {
                    "id": measure.id,
                    "name": measure.name
                } if measure else None
            }
        })

    return Response({
        'code': 200,
        'status': True,
        'message': 'Consulta realizada Exitosamente',
        'data': data
        })







