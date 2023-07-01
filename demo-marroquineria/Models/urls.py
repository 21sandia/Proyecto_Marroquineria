from django.urls import path
from Models import views
from Models.controllers import viewsUser
#nuevo

urlpatterns = [
    path('roles/', views.list_role, name='list_role'),
    path('roles/create/', views.create_role, name='create_role'),
    path('roles/update/<int:pk>/', views.update_role, name='update_role'),
    path('roles/delete/<int:pk>/', views.delete_role, name='delete_role'),
    
    path('people/', viewsUser.list_people, name='list_people'),
    path('people/create/', viewsUser.create_people, name='create_people'),
    path('people/update/<int:pk>/', viewsUser.update_people, name='update_people'),
    path('people/delete/<int:pk>/', viewsUser.delete_people, name='delete_people'),
    
    path('categories/', views.list_category, name='list_category'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/update/<int:pk>/', views.update_category, name='update_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('type_prod/', views.list_type_prod, name='list_type_prod'),
    path('type_prod/create/', views.create_type_prod, name='create_type_prod'),
    path('type_prod/update/<int:pk>/', views.update_type_prod, name='update_type_prod'),
    path('type_prod/delete/<int:pk>/', views.delete_type_prod, name='delete_type_prod'),
    
    path('products/', views.list_product, name='list_product'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:pk>/', views.update_product, name='update_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('orders/', views.list_order, name='list_order'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/update/<int:pk>/', views.update_order, name='update_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    
    path('carts/', views.list_carts, name='list_carts'),
    path('carts/create/', views.create_carts, name='create_carts'),
    path('carts/update/<int:pk>/', views.update_carts, name='update_carts'),
    path('carts/delete/<int:pk>/', views.delete_carts, name='delete_carts'),
    
    path('detail_sales/', views.list_detail_sale, name='list_detail_sale'),
    path('detail_sales/create/', views.create_detail_sale, name='create_detail_sale'),
    path('detail_sales/update/<int:pk>/', views.update_detail_sale, name='update_detail_sale'),
    path('detail_sales/delete/<int:pk>/', views.delete_detail_sale, name='delete_detail_sale'),
    
    path('list-users/', views.list_users, name='list_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('update-user/<int:pk>/', views.update_user, name='update_user'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
]
