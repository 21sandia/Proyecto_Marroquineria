from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from Models.controllers import viewsRol, viewsCategory , viewsPeople, viewsProduct, viewsState, viewsTypeProd, viewsDetailProd, viewsGetAllDetaProd, viewsUser
from Models.controllers import viewsSale, viewsDetailSale, viewsGetAllDataProd, viewsUserGetAllData, viewsGetAllDetSale
from Models.controllers import viewsRecupContrasena
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Estados
    path('list-state/', viewsState.list_States, name='list_state'), # Listar 
    path('create-state/', viewsState.create_States, name='create_state'), # Crear
    path('update-state/<int:pk>/', viewsState.update_States, name='update_state'), # Editar
    path('delete-state/<int:pk>/', viewsState.delete_States, name='delete_state'), # Eliminar

    # Roles
    path('list-rol/', viewsRol.list_rol, name='list_rol'), # Listar
    path('create-rol/', viewsRol.create_rol, name='create_rol'), # Crear
    path('update-rol/<int:pk>/', viewsRol.update_rol, name='update_rol'), # Editar
    path('delete-rol/<int:pk>/', viewsRol.delete_rol, name='delete_rol'), # Eliminar

    # Categorías
    path('list-category/', viewsCategory.list_category, name='list_category'), # Listar
    path('create-category/', viewsCategory.create_category, name='create_category'), # Crear
    path('update-category/<int:pk>/', viewsCategory.update_category, name='update_category'), # Editar
    path('delete-category/<int:pk>/', viewsCategory.delete_category, name='delete_category'), # Eliminar

    # Tipo de productos 
    path('list-type_prod/', viewsTypeProd.list_type_prod, name='list_type_prod'), # Listar
    path('create-type_prod/', viewsTypeProd.create_type_prod, name='create_type_prod'), # Crear
    path('update-type_prod/<int:pk>/', viewsTypeProd.update_type_prod, name='update_type_prod'), # Editar
    path('delete-type_prod/<int:pk>/', viewsTypeProd.delete_type_prod, name='delete_type_prod'), # Eliminar

    # Productos
    path('list-product/', viewsProduct.list_product, name='list_product'), # Listar
    path('create-product/', viewsProduct.create_product, name='create_product'), # Crear
    path('update-product/<int:pk>/', viewsProduct.update_product, name='update_product'), # Editar
    path('delete-product/<int:pk>/', viewsProduct.delete_product, name='delete_product'), # Eliminar
    
    # Detalle de producto
    path('list-detail_prod/', viewsDetailProd.list_detailProd, name='list_detail_prod'), # Listar
    path('create-detail_prod/', viewsDetailProd.create_detailProd, name='create_detail_prod'), # Crear
    path('update-detail_prod/<int:pk>/', viewsDetailProd.update_detailProd, name='update_detail_prod'), # Editar
    path('delete-detail_prod/<int:pk>/', viewsDetailProd.delete_detailProd, name='delete_detail_prod'), # Eliminar

    # Trae toda la información de las tablas relacionadas con el producto
    path('get-all-data_prod/', viewsGetAllDataProd.get_all_models_data, name='get_all_data'), 



    # Trae la información relacionada del producto con detalle de producto
    path('get-all-detal_prod/', viewsGetAllDetaProd.get_all_datap, name='get_all_data'), 

    # ventas
    path('list-sales/', viewsSale.list_sale, name='list_sale'), # Listar 
    path('create-sales/', viewsSale.create_sale, name='create_sale'), # Crear
    path('update-sales/<int:pk>/', viewsSale.update_sale, name='update_sale'), # Editar
    path('delete-sales/<int:pk>/', viewsSale.delete_sale, name='delete_sale'), # Eliminar
    
    # Detalle ventas
    path('list-detail_sales/', viewsDetailSale.list_detail_sale, name='list_detail_sale'), # Listar 
    path('create-detail_sales/', viewsDetailSale.create_detail_sale, name='create_detail_sale'), # Crear
    path('update-detail_sales/<int:pk>/', viewsDetailSale.update_detail_sale, name='update_detail_sale'), # Editar
    path('delete-detail_sales/<int:pk>/', viewsDetailSale.delete_detail_sale, name='delete_detail_sale'), # Eliminar

    # Trae la información relacionada de la venta con detalle de la venta
    path('get-all-det_sales/', viewsGetAllDetSale.get_all_datasale, name='get_all_data_sales'), 

    # Peoples
    path('list-people/', viewsPeople.list_people, name='list_people'), # Listar 
    path('create-people/', viewsPeople.create_people, name='create_people'), # Crear
    path('update-people/<int:pk>/', viewsPeople.update_people, name='update_people'), # Editar
    path('delete-people/<int:pk>/', viewsPeople.delete_people, name='delete_people'), # Eliminar

    # Usuarios
    path('list-user/', viewsUser.list_user, name='list_user'), # Listar 
    path('create-user/', viewsUser.create_user, name='create_user'), # Crear
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'), # Editar
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'), # Eliminar

    # Trae toda la información de las tablas relacionadas con el usuario 
    path('get_all_dataUser/', viewsUserGetAllData.get_related_foreign_keys, name='get_all_models_data'), # Trae todos los datos de views User get_all_data

    #  **RECUPERAR CONTRASEÑA**
    path('recup_contrasena/', viewsRecupContrasena.recuperar_contrasena, name='recuperar_contrasena'), #  
    path('cambiar_contrasena/<str:uidb64>/<str:token>/', viewsRecupContrasena.cambiar_contrasena, name='cambiar_contrasena'), #  

    # **Token**
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # link Ingreso usuario, para generar token
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
