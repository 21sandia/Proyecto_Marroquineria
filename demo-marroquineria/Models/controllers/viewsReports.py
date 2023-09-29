import csv
import xlsxwriter
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count, Case, When, IntegerField, Avg
from django.http import  HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta
from ..models import Sales, Products, DetailSales


# Función para exportar estadísticas a CSV
def export_to_csv(data, filename, headers):
    # Crear una respuesta HTTP con el tipo de contenido "text/csv"
    response = HttpResponse(content_type='text/csv')
    # Definir el encabezado Content-Disposition para indicar que es un archivo adjunto CSV con un nombre de archivo específico
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    # Crear un escritor CSV para escribir los datos en la respuesta
    writer = csv.writer(response)
    # Escribir la fila de encabezados
    writer.writerow(headers)

    # Iterar sobre los datos y escribir cada fila en el archivo CSV
    for item in data:
        writer.writerow(item)

    # Devolver la respuesta HTTP con el archivo CSV
    return response

# Función para exportar estadísticas a Excel
def export_to_excel(data, filename, headers):
    # Crear una respuesta HTTP con el tipo de contenido "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # Definir el encabezado Content-Disposition para indicar que es un archivo adjunto de Excel con un nombre de archivo específico
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

    # Crear un objeto de libro de Excel y una hoja de trabajo dentro de él
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # Definir un formato en negrita para los encabezados
    bold = workbook.add_format({'bold': True})

    # Escribir los encabezados en la primera fila de la hoja de trabajo en negrita
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, bold)

    # Escribir los datos en la hoja de trabajo
    for row_num, row_data in enumerate(data, start=1):
        for col_num, cell_value in enumerate(row_data):
            worksheet.write(row_num, col_num, cell_value)

    # Cerrar el libro de Excel
    workbook.close()

    # Devolver la respuesta HTTP con el archivo de Excel
    return response

# Función para generar el informe de ventas
@api_view(['GET'])
def sales_report(request):
    # Obtener las fechas de inicio y fin desde los datos de la solicitud
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Verificar que se proporcionen ambas fechas
    if not start_date or not end_date:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Debes proporcionar una fecha de inicio y una fecha de fin.',
            'status': True
        }
        return Response(response_data)

    try:
        # Intentar convertir las fechas en objetos datetime con el formato YYYY-MM-DD
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Las fechas deben tener el formato YYYY-MM-DD.',
            'status': True
        }
        return Response(response_data)

    # Calcular la diferencia de días entre las fechas de inicio y fin
    date_difference = end_date - start_date

    # Verificar que la fecha de inicio sea anterior a la fecha de fin
    if date_difference.days < 0:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'La fecha de inicio debe ser anterior a la fecha de fin.',
            'status': True
        }
        return Response(response_data)

    # Filtrar las ventas de acuerdo con el rango de fechas especificado
    if date_difference.days == 0:
        sales = Sales.objects.filter(date=start_date)
    elif date_difference.days <= 7:
        sales = Sales.objects.filter(date__range=(start_date, end_date))
    elif date_difference.days <= 15:
        end_date = start_date + timedelta(days=14)
        sales = Sales.objects.filter(date__range=(start_date, end_date))
    elif date_difference.days <= 30:
        sales = Sales.objects.filter(date__year=start_date.year, date__month=start_date.month)
    else:
        sales = Sales.objects.filter(date__range=(start_date, end_date))

    # Calcular el total de ventas en el período especificado
    total_sales = sales.aggregate(total_sales=Sum('total_sale'))['total_sales']

    if total_sales is not None:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Consulta realizada exitosamente',
            'status': True,
            'data': {'total_sales': total_sales}
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay ventas registradas en el período especificado.',
            'status': True,
            'data': {'total_sales': 0}
        }

    # Obtener el formato de exportación seleccionado por el usuario
    export_format = request.data.get('export_format')
    if export_format == 'csv':
        # Exportar a CSV
        data = [['Ventas Totales'], [total_sales]]
        headers = ['Ventas Totales']
        return export_to_csv(data, 'sales_report', headers)
    elif export_format == 'excel':
        # Exportar a Excel
        data = [['Ventas Totales'], [total_sales]]
        headers = ['Ventas Totales']
        return export_to_excel(data, 'sales_report', headers)
    else:
        return Response(response_data)

@api_view(['GET'])
def generate_product_sales_report(request):
    # Obtener las fechas de inicio y fin desde los datos de la solicitud
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    # Verificar que se proporcionen ambas fechas
    if not start_date or not end_date:
        return Response({'code': status.HTTP_200_OK,
                            'message': 'Debes proporcionar una fecha de inicio y una fecha de fin.',
                            'status': True})

    try:
        # Intentar convertir las fechas en objetos datetime con el formato YYYY-MM-DD
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return Response({'code': status.HTTP_200_OK,
                            'message': 'Las fechas deben tener el formato YYYY-MM-DD.',
                            'status': True})

    # Calcular la diferencia de días entre las fechas de inicio y fin
    date_difference = end_date - start_date

    # Verificar que la fecha de inicio sea anterior a la fecha de fin
    if date_difference.days < 0:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'La fecha de inicio debe ser anterior a la fecha de fin.',
            'status': True
        }
        return Response(response_data)

    # Filtrar las ventas de acuerdo con el rango de fechas especificado
    if date_difference.days == 0:
        sales = Sales.objects.filter(date=start_date)
    elif date_difference.days <= 7:
        sales = Sales.objects.filter(date__range=(start_date, end_date))
    elif date_difference.days <= 15:
        end_date = start_date + timedelta(days=14)
        sales = Sales.objects.filter(date__range=(start_date, end_date))
    elif date_difference.days <= 30:
        sales = Sales.objects.filter(date__year=start_date.year, date__month=start_date.month)
    else:
        sales = Sales.objects.filter(date__range=(start_date, end_date))

    # Obtener los productos más vendidos y sus estadísticas
    top_products = DetailSales.objects.filter(fk_id_sale__in=sales).values('fk_id_prod__id', 'fk_id_prod__name').annotate(
        total_sales=Sum(F('quantity') * F('price_unit')),
        sales_count=Count('id'),
        average_sales=Avg(F('quantity') * F('price_unit'))
    ).order_by('-total_sales')[:5]

    # Obtener todos los productos y sus estadísticas
    all_products = Products.objects.all()
    product_sales = all_products.annotate(
        total_sales=ExpressionWrapper(
            Sum(Case(
                When(detailsales__fk_id_sale__in=sales, then=F('detailsales__quantity') * F('detailsales__price_unit')),
                default=0,
                output_field=DecimalField()
            )),
            output_field=DecimalField()
        ),
        sales_count=Count('detailsales'),
        average_sales=ExpressionWrapper(
        Avg(Case(
            When(detailsales__fk_id_sale__in=sales, then=F('detailsales__quantity') * F('detailsales__price_unit')),
            default=0,
            output_field=DecimalField()
        )),
        output_field=DecimalField()
    )).values('id', 'name', 'total_sales', 'sales_count', 'average_sales').order_by('total_sales')[:5]

    # Preparar la respuesta JSON con los resultados
    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Consulta realizada exitosamente',
        'status': True,
        'top_products': [{'product_id': item['fk_id_prod__id'], 'product_name': item['fk_id_prod__name'], 'total_sales': item['total_sales'], 'sales_count': item['sales_count'], 'average_sales': item['average_sales']} for item in top_products],
        'bottom_products': [{'product_id': item['id'], 'product_name': item['name'], 'total_sales': item['total_sales'], 'sales_count': item['sales_count'], 'average_sales': item['average_sales']} for item in product_sales]
    }

    # Obtener el formato de exportación seleccionado por el usuario
    export_format = request.data.get('export_format')
    if export_format == 'csv':
        # Exportar a CSV
        data = [['ID de Producto', 'Nombre de Producto', 'Ventas Totales', 'Cantidad de Ventas', 'Ventas Promedio']]
        data.extend([[item['product_id'], item['product_name'], item['total_sales'], item['sales_count'], item['average_sales']] for item in top_products])
        headers = ['ID de Producto', 'Nombre de Producto', 'Ventas Totales', 'Cantidad de Ventas', 'Ventas Promedio']
        return export_to_csv(data, 'product_sales_report', headers)
    elif export_format == 'excel':
        # Exportar a Excel
        data = [['ID de Producto', 'Nombre de Producto', 'Ventas Totales', 'Cantidad de Ventas', 'Ventas Promedio']]
        data.extend([[item['product_id'], item['product_name'], item['total_sales'], item['sales_count'], item['average_sales']] for item in top_products])
        headers = ['ID de Producto', 'Nombre de Producto', 'Ventas Totales', 'Cantidad de Ventas', 'Ventas Promedio']
        return export_to_excel(data, 'product_sales_report', headers)
    else:
        return Response(response_data)






