from django.core.mail import EmailMessage
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from reportlab.lib.units import cm 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO
from ..models import *
from ..serializers import *


@api_view(['POST'])
def create_sale_detail(request):
    # Obtener los datos de la solicitud
    state_id = request.data.get('fk_id_state')
    people_id = request.data.get('fk_id_people')
    name = request.data.get('name')
    document = request.data.get('document')
    products = request.data.get('products', [])
    
    # Verificar si se proporcionaron valores para los campos state_id y people_id
    state = None
    if state_id:
        try:
            state = States.objects.get(id=state_id)  # Obtener el estado correspondiente
        except States.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Estado no encontrado.",
                "status": False})

    people = None
    if people_id:
        try:
            people = Peoples.objects.get(id=people_id)  # Obtener la persona correspondiente
        except Peoples.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Persona no encontrada.",
                "status": False
            })
    else:
        # Create a new People object for unregistered user
        people = Peoples.objects.create(is_guest=True, name=name, document=document)

    total_sale = 0
    detail_data_list = []
    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')
        try:
            # Buscar el producto asociado
            product = Products.objects.get(id=product_id)  # Obtener el producto correspondiente
        except Products.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": f"El producto con el id {product_id} no existe.",
                "status": False})
        # Verificar campos obligatorios en los detalles del producto
        if not product_id or not quantity:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Campos obligatorios faltantes en los detalles del producto: product_id, quantity.",
                "status": False})
        # Verificar si hay suficiente stock
        if quantity > product.quantity:
            return Response({
                "code": status.HTTP_200_OK,
                "message": f"No hay suficiente stock para el producto {product.name}.",
                "status": False})
        # Actualizar la cantidad de productos
        product.quantity -= quantity  # Restar la cantidad vendida del stock del producto
        product.save()  # Guardar los cambios en el producto
        # Calcular el subtotal del producto
        subtotal_product = product.price_sale * quantity  # Calcular el subtotal del producto
        total_sale += subtotal_product  # Sumar el subtotal al total de la venta
        # Crear datos para el detalle del producto
        detail_data = {
            'fk_id_sale': None,  # Se establecerá después de crear la venta
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': product.price_sale,
            'total_product': subtotal_product,}
        detail_data_list.append(detail_data)  # Agregar los detalles del producto a la lista
    # Crear una nueva venta
    sale_data = {
        'fk_id_state': state.id if state else None,
        'fk_id_people': people.id if people else None,
        'total_sale': total_sale,}
    sale_serializer = SaleSerializer(data=sale_data)  # Crear una instancia del serializador de ventas
    if sale_serializer.is_valid():
        sale = sale_serializer.save()  # Guardar la venta en la base de datos
        # Actualizar el campo fk_id_sale en los detalles del producto
        for detail_data in detail_data_list:
            detail_data['fk_id_sale'] = sale
        # Crear los detalles de venta en la base de datos
        DetailSales.objects.bulk_create([DetailSales(**data) for data in detail_data_list])

        # Crear el PDF con los detalles de la compra
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        pdf_content = []
        pdf_content.append(Paragraph(f'Comprobante de compra - Factura #{sale.id}', styles['Title']))

        # Agregar datos del Marketplace, cliente, etc.
        pdf_content.append(Paragraph(f'Marketplace Ecommerce.com', styles['Normal']))
        pdf_content.append(Paragraph(f'Cliente: {people.name}', styles['Normal']))
        pdf_content.append(Paragraph(f'Teléfono: {people.phone}', styles['Normal']))
        pdf_content.append(Paragraph(f'Correo: {people.email}', styles['Normal']))
        pdf_content.append(Paragraph(f'Dirección: {people.address}', styles['Normal']))

        data = [['Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']]
        for detail in detail_data_list:
            product = detail['fk_id_prod']
            quantity = detail['quantity']
            subtotal_product = detail['total_product']
            data.append([product.name, quantity, f"${product.price_sale}", f"${subtotal_product}"])

        total_row = ['Total de la compra', '', '', f"${total_sale}"]
        data.append(total_row)

        table_style = TableStyle([])
        table = Table(data, colWidths=[4 * cm, 2 * cm, 3 * cm, 3 * cm])
        table.setStyle(table_style)
        pdf_content.append(table)

        doc.build(pdf_content)
        buffer.seek(0)

        # Adjuntar el PDF al correo electrónico
        email = EmailMessage(
            'Comprobante de compra',
            f'Querido(a) {people.name}, te informamos que tu compra con número de factura: {sale.id} ha sido captada con éxito.\n',
            'ecommerce.marquetp@gmail.com',
            [people.email],
        )
        email.attach('comprobante.pdf', buffer.read(), 'application/pdf')
        email.send()

        return Response({"code": status.HTTP_200_OK,
                         "message": "Venta creada exitosamente. Se ha enviado un correo de notificación con el comprobante PDF adjunto.",
                         "status": True,
                         "data": sale_serializer.data})
    else:
        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# **Lista los datos de venta junto con detalle venta**
@api_view(['GET'])
def list_sale_detail(request):
     # Obtener los parámetros de filtrado de la solicitud
    customer_id = request.query_params.get('customer_id', None)
    state_id = request.query_params.get('state_id', None)
    min_total_sale = request.query_params.get('min_total_sale', None)
    max_total_sale = request.query_params.get('max_total_sale', None)
    start_date_str = request.query_params.get('start_date', None)
    end_date_str = request.query_params.get('end_date', None)

    # Convertir las fechas en objetos datetime si se proporcionan
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = None

    # Filtrar ventas según los parámetros proporcionados
    sales_query = Q()
    # Por cliente
    if customer_id:
        sales_query &= Q(fk_id_people=customer_id)
    # Por estado
    if state_id:
        sales_query &= Q(fk_id_state=state_id)
    # Por total mínimo
    if min_total_sale:
        sales_query &= Q(total_sale__gte=min_total_sale)
    # Por total máximo
    if max_total_sale:
        sales_query &= Q(total_sale__lte=max_total_sale)
    # Por rango de fecha
    if start_date:
        sales_query &= Q(date__gte=start_date)
    if end_date:
        sales_query &= Q(date__lte=end_date)

    sales = Sales.objects.filter(sales_query)

    if not sales:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "No hay ventas registradas.",
            "status": True})

    response_data = []

    for sale in sales:
        sale_serializer = SaleSerializer(sale)
        
        details = DetailSales.objects.filter(fk_id_sale=sale)
        detail_serializer = DetailSaleSerializer(details, many=True)
        
        sale_data = {
            "sale": sale_serializer.data,
            "details": detail_serializer.data,
        }
        
        response_data.append(sale_data)

    return Response({
        "code": status.HTTP_200_OK,
        "message": "Consulta realizada exitosamente.",
        "status": True,
        "data": response_data})


# **Edita la venta junto con el detalle de venta**
@api_view(['PATCH'])
def edit_sale_detail(request, pk):
    # Obtén los datos de la solicitud
    state_id = request.data.get('fk_id_state')
    people_id = request.data.get('fk_id_people')
    products = request.data.get('products', [])

    # Verificar si la venta existe
    try:
        sale = Sales.objects.get(pk=pk)
    except Sales.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Venta no encontrada.",
            "status": True})

    # Validar si el estado y la persona existen
    try:
        state = States.objects.get(id=state_id)
    except States.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Estado no encontrado.",
            "status": True})

    try:
        people = Peoples.objects.get(id=people_id)
    except Peoples.DoesNotExist:
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Persona no encontrada.",
            "status": True})

    # Actualizar la entidad de venta
    sale.fk_id_state = state
    sale.fk_id_people = people

    # Calcular el monto total de la venta
    total_sale = 0
    detail_data_list = []

    for product_data in products:
        product_id = product_data.get('product_id')
        quantity = product_data.get('quantity')

        # Validar si el producto existe
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Producto no encontrado.",
                "status": True})

        price_unit = product.price_sale
        total_product = price_unit * quantity
        total_sale += total_product

        # Actualizar la cantidad en el producto
        product.quantity -= quantity
        product.save()

        detail_data = {
            'fk_id_sale': sale,
            'fk_id_prod': product,
            'quantity': quantity,
            'price_unit': price_unit,
            'total_product': total_product,
        }

        detail_data_list.append(detail_data)

    # Actualizar el atributo total_sale de la venta
    sale.total_sale = total_sale

    # Eliminar los registros de detalles existentes asociados con la venta
    DetailSales.objects.filter(fk_id_sale=sale).delete()

    # Guardar la entidad de venta actualizada
    sale.save()

    # Crear detalles de venta en masa
    DetailSales.objects.bulk_create([DetailSales(**data) for data in detail_data_list])

    # Devolver los datos actualizados de la venta
    sale_serializer = SaleSerializer(sale)
    return Response({
        "code": status.HTTP_200_OK,
        "message": "Venta actualizada exitosamente.",
        "status": True,
        "data": sale_serializer.data})


@api_view(['DELETE'])
def delete_sale_detail(request, pk):
    try:
        sale = Sales.objects.get(pk=pk)
        
        # Obtener los detalles de la venta
        sale_details = DetailSales.objects.filter(fk_id_sale=sale)

        # Eliminar los registros de detalles existentes asociados con la venta
        sale_details.delete()

        # Eliminar la venta
        sale.delete()

        # Aumentar la cantidad de productos en la entidad de productos
        for sale_detail in sale_details:
            product = sale_detail.fk_id_prod
            quantity = sale_detail.quantity

            # Aumentar la cantidad en el producto
            product.quantity += quantity
            product.save()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Eliminada exitosamente', 
                              'status': True})

    except Sales.DoesNotExist:
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'No encontrado', 
                              'status': True})

    except Exception as e:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Error del servidor', 
                              'status': True})
