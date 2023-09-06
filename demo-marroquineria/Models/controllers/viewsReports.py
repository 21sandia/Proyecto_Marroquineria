import pandas as pd
from datetime import datetime, timedelta  
from django.db.models import Sum, Q
from django.http import JsonResponse  
from django.db.models.functions import TruncDate  
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status 
from ..models import Sales, DetailSales  

from datetime import datetime, timedelta
from django.shortcuts import HttpResponse, JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models import Q
from .models import Sales

def sales_report(request, report_type, start_date, end_date):
    # Convierte las cadenas de fecha en objetos datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Determinar el tipo de informe y generar el informe correspondiente
    if report_type in ('mensual', 'quincenal', 'semanal', 'diario'):
        # Procesar los argumentos y generar el informe según el tipo de informe
        sales = generate_sales_report(report_type, start_date, end_date)
    else:
        return HttpResponse('Tipo de informe no válido')

    return JsonResponse({
        "code": 200,
        "message": f"Reporte {report_type} generado exitosamente.",
        "status": True,
        "data": sales
    })

def generate_sales_report(report_type, start_date, end_date):
    sales_query = Q()  # Consulta para filtrar ventas

    if start_date:
        sales_query &= Q(date__gte=start_date)  # Filtrar ventas con fecha mayor o igual a la fecha de inicio
    if end_date:
        end_date += timedelta(days=1)  # Añadir un día a la fecha de fin para incluir ventas hasta ese día
        sales_query &= Q(date__lt=end_date)  # Filtrar ventas con fecha menor a la fecha de fin (exclusivo)

    # Obtener las ventas según el rango de fechas y la frecuencia
    sales = Sales.objects.filter(sales_query).annotate(date_group=TruncDate('date')).values('date_group').annotate(total_sales=Sum('total_sale')).order_by('date_group')

    response_data = []  # Inicializar una lista para almacenar los datos de respuesta

    if report_type == 'diario':
        for sale in sales:
            response_data.append({
                'date': sale['date_group'].strftime('%Y-%m-%d'),  # Formatear la fecha como 'YYYY-MM-DD'
                'total_sales': sale['total_sales'],  # Total de ventas para la fecha
            })
    elif report_type == 'semanal':
        for sale in sales:
            response_data.append({
                'start_date': sale['date_group'].strftime('%Y-%m-%d'),  # Formatear la fecha de inicio como 'YYYY-MM-DD'
                'end_date': (sale['date_group'] + timedelta(days=6)).strftime('%Y-%m-%d'),  # Calcular la fecha de fin (6 días después) y formatear como 'YYYY-MM-DD'
                'total_sales': sale['total_sales'],  # Total de ventas para la semana
            })
    elif report_type == 'quincenal':
        for sale in sales:
            response_data.append({
                'start_date': sale['date_group'].strftime('%Y-%m-%d'),  # Formatear la fecha de inicio como 'YYYY-MM-DD'
                'end_date': (sale['date_group'] + timedelta(days=13)).strftime('%Y-%m-%d'),  # Calcular la fecha de fin (13 días después) y formatear como 'YYYY-MM-DD'
                'total_sales': sale['total_sales'],  # Total de ventas para la quincena
            })
    elif report_type == 'mensual':
        for sale in sales:
            response_data.append({
                'month': sale['date_group'].strftime('%Y-%m'),  # Formatear el mes como 'YYYY-MM'
                'total_sales': sale['total_sales'],  # Total de ventas para el mes
            })

    return response_data