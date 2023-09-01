from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from ..models import Sales, DetailSales, Products




@api_view(['GET'])
def sales_statistics(request):
    # Obtener los parámetros de filtrado de la solicitud
    start_date_str = request.query_params.get('start_date', None)
    end_date_str = request.query_params.get('end_date', None)
    report_type = request.query_params.get('report_type', None)

    # Convertir las fechas en objetos datetime si se proporcionan
    if start_date_str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = None

    # Realizar el filtrado de ventas según los parámetros proporcionados
    sales_query = Q()
    if start_date:
        sales_query &= Q(date__gte=start_date)
    if end_date:
        sales_query &= Q(date__lt=end_date + datetime.timedelta(days=1))

    sales = Sales.objects.filter(sales_query)

    if not sales:
        return Response({"code": status.HTTP_200_OK,
                         "message": "No hay ventas registradas.",
                         "status": True
                         })

    # Crear un DataFrame de pandas para manipular los datos
    data = []
    for sale in sales:
        details = DetailSales.objects.filter(fk_id_sale=sale)
        total_products = details.aggregate(total_products=Sum('quantity'))['total_products']
        data.append({
            "sale_id": sale.id,
            "total_products": total_products,
            "total_sale": float(sale.total_sale),  # Convertir a punto flotante
            "date": sale.date,
        })

    df = pd.DataFrame(data)

    # Convertir la columna 'date' a formato datetime
    df['date'] = pd.to_datetime(df['date'])

    # Generar gráficos (ventas por día) si se solicita
    if report_type == 'daily' or report_type == 'all':
        df['day'] = df['date'].dt.to_period('D')
        daily_sales = df.groupby('day')['total_sale'].sum()
        daily_sales.plot(kind='bar')
        plt.xlabel('Día')
        plt.ylabel('Total Ventas')
        plt.title('Ventas por Día')
        plt.xticks(rotation=45)
        plt.savefig('daily_sales.png')  # Guardar el gráfico como imagen
        plt.close()  # Cerrar el gráfico para liberar memoria

    # Generar gráficos (ventas por semana) si se solicita
    if report_type == 'weekly' or report_type == 'all':
        df['week'] = df['date'].dt.to_period('W')
        weekly_sales = df.groupby('week')['total_sale'].sum()
        weekly_sales.plot(kind='bar')
        plt.xlabel('Semana')
        plt.ylabel('Total Ventas')
        plt.title('Ventas por Semana')
        plt.xticks(rotation=45)
        plt.savefig('weekly_sales.png')  # Guardar el gráfico como imagen
        plt.close()  # Cerrar el gráfico para liberar memoria


    # Generar gráficos (ventas por mes) si se solicita
    if report_type == 'monthly' or report_type == 'both':
        df['month'] = df['date'].dt.to_period('M')
        monthly_sales = df.groupby('month')['total_sale'].sum()
        monthly_sales.plot(kind='bar')
        plt.xlabel('Mes')
        plt.ylabel('Total Ventas')
        plt.title('Ventas por Mes')
        plt.xticks(rotation=0)
        plt.savefig('monthly_sales.png')  # Guardar el gráfico como imagen
        plt.close()  # Cerrar el gráfico para liberar memoria

    # Generar gráficos (ventas por año) si se solicita
    if report_type == 'yearly' or report_type == 'both':
        df['year'] = df['date'].dt.to_period('Y')
        yearly_sales = df.groupby('year')['total_sale'].sum()
        yearly_sales.plot(kind='bar')
        plt.xlabel('Año')
        plt.ylabel('Total Ventas')
        plt.title('Ventas por Año')
        plt.xticks(rotation=45)
        plt.savefig('yearly_sales.png')  # Guardar el gráfico como imagen
        plt.close()  # Cerrar el gráfico para liberar memoria

    # Generar un índice completo de días
    full_day_index = pd.period_range(start=start_date, end=end_date, freq='D')

    # Reindexar las ventas diarias con el índice completo
    daily_sales = daily_sales.reindex(full_day_index, fill_value=0)

    # Ahora puedes trazar las ventas diarias como antes
    daily_sales.plot(kind='bar')

    # Generar reporte en formato JSON
    report_data = {
        "total_sales": df['sale_id'].nunique(),
        "total_revenue": df['total_sale'].sum(),
        # Agregar más estadísticas según sea necesario
    }

    return Response({"code": status.HTTP_200_OK,
                     "message": f"Reporte generado exitosamente para: {report_type}",
                     "status": True,
                     "data": report_data,
                     })


@api_view(['GET'])
def sales_report(request, interval, report_type, start_year=None, start_month=None, end_year=None, end_month=None, product_id=None):
    # Determinar cómo agrupar las fechas según el intervalo (semana, mes, año)
    if interval == 'week':
        grouping = TruncWeek('date')
    elif interval == 'month':
        grouping = TruncMonth('date')
    elif interval == 'year':
        grouping = TruncYear('date')
    else:
        return Response({'code': status.HTTP_400_BAD_REQUEST,
                         'status': False,
                         'message': 'Intervalo inválido',
                         'data': []
                         })

    # Obtener las ventas agrupadas por fecha y producto
    sales = DetailSales.objects.annotate(date_grouped=grouping).values('date_grouped', 'fk_id_prod').annotate(total_sold=Count('id')).order_by('date_grouped', '-total_sold')

    # Aplicar filtros de inicio y fin de año/mes, y producto si están presentes en los parámetros
    if start_year:
        sales = sales.filter(date_grouped__year__gte=start_year)
    if start_month:
        sales = sales.filter(date_grouped__month__gte=start_month)
    if end_year:
        sales = sales.filter(date_grouped__year__lte=end_year)
    if end_month:
        sales = sales.filter(date_grouped__month__lte=end_month)
    if product_id:
        sales = sales.filter(fk_id_prod=product_id)

    sales_data = []

    # Construir la lista de datos de ventas con información relevante
    for sale in sales:
        product = Products.objects.get(pk=sale['fk_id_prod'])
        product_data = {
            "product_id": product.id,
            "product_name": product.name,
            "total_sold": sale['total_sold'],
            "date": sale['date_grouped']
        }
        sales_data.append(product_data)

    sales_data.sort(key=lambda x: x['total_sold'], reverse=True)  # Ordenar los datos por ventas descendentes

    # Seleccionar los datos según el tipo de informe (top o bottom)
    if report_type == 'top':
        sales_data = sales_data[:5]  # Tomar los 5 productos más vendidos
    elif report_type == 'bottom':
        sales_data = sales_data[-5:]  # Tomar los 5 productos menos vendidos

    # Construir la respuesta en el formato deseado
    return Response({'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'El informe se ha generado exitosamente',
                    'data': sales_data})  

