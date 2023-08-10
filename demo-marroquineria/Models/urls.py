from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from Models.controllers import viewsRol, viewsCategory , viewsPeople, viewsProduct, viewsState, viewsTypeProd, viewsProductDetail, viewsUser
from Models.controllers import viewsSale, viewsDetailSale, viewsUserGetAllData
from Models.controllers import viewsRecupContrasena
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # ** Estados **

    # Listar Estados
    path('list-state/', viewsState.list_States, name='list_state'), 
    # Crear Estados
    path('create-state/', viewsState.create_States, name='create_state'), 
    # Editar Estados
    path('update-state/<int:pk>/', viewsState.update_States, name='update_state'),
    # Eliminar Estados
    path('delete-state/<int:pk>/', viewsState.delete_States, name='delete_state'), 

    # ** Roles **

    # Listar Rol
    path('list-rol/', viewsRol.list_rol, name='list_rol'),
    # Crear Rol
    path('create-rol/', viewsRol.create_rol, name='create_rol'),
    # Editar Rol
    path('update-rol/<int:pk>/', viewsRol.update_rol, name='update_rol'), 
    # Eliminar Rol
    path('delete-rol/<int:pk>/', viewsRol.delete_rol, name='delete_rol'),

    # ** Peoples **

    # Listar People
    path('list-people/', viewsPeople.list_people, name='list_people'),
    # Crear People
    path('create-people/', viewsPeople.create_people, name='create_people'), 
    # Editar People
    path('update-people/<int:pk>/', viewsPeople.update_people, name='update_people'),
    # Eliminar People
    path('delete-people/<int:pk>/', viewsPeople.delete_people, name='delete_people'),

    # ** Usuarios **

    # Listar Usuario
    path('list-user/', viewsUser.list_user, name='list_user'),
    # Crear Usuario
    path('create-user/', viewsUser  .create_user, name='create_user'), 
    # Editar Usuario
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'), 
    # Eliminar Usuario
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'), 

    # Trae toda la información de las tablas relacionadas con el usuario 
    path('get_all_dataUser/', viewsUserGetAllData.get_related_foreign_keys, name='get_all_models_data'),

    # ** Categorías **

    # Listar Category
    path('list-category/', viewsCategory.list_category, name='list_category'), 
    # Crear Category
    path('create-category/', viewsCategory.create_category, name='create_category'),
    # Editar Category
    path('update-category/<int:pk>/', viewsCategory.update_category, name='update_category'), 
    # Eliminar Category
    path('delete-category/<int:pk>/', viewsCategory.delete_category, name='delete_category'),

    # Tipo de productos 

    # Lista categoría con tipo de producto
    path('get_all_tpcateg/', viewsTypeProd.get_all_tpcateg, name='ListaCategTProd'),
    # Lista solo el tipo de producto 
    path('list-type_prod/', viewsTypeProd.list_type_prod, name='list-type_prod'),
    # Crear tipo de producto
    path('create-type_prod/', viewsTypeProd.create_type_prod, name='create_type_prod'), 
    # Editar tipo de producto
    path('update-type_prod/<int:pk>/', viewsTypeProd.update_type_prod, name='update_type_prod'),
    # Eliminar tipo de producto
    path('delete-type_prod/<int:pk>/', viewsTypeProd.delete_type_prod, name='delete_type_prod'), 

    # Trae toda la información relacionada con categoría y tipo de producto
    #path('get_all_tpcateg/', viewsTpCategory.get_all_tpcateg, name='get_all_tpcateg'),

    # ** Productos **
 
    # Listar todos los modelos relacionados con Producto
    path('get-Product/', viewsProduct.get_all_models_data, name='Estado-categ-tipo-producto'), 
     # Lista todo el producto completo con el Detalle Producto
    path('get-all-Product/', viewsProduct.get_all_models_prod_detailp, name='Estado-categ-tipo-producto-detalleProducto'),
    
    


    # ** Producto con Detalle Producto **

    # Crea el Producto con el Detalle de Producto
    path('create-product/', viewsProductDetail.product_create, name='crear_producto_detalle_product'),
    # lista el Producto con Detalle Producto y Estado
    path('list-product/', viewsProductDetail.product_details, name='product-details'),
    # Edita el Producto con el Detalle de Producto
    path('update-product/<int:pk>/', viewsProductDetail.edit_product, name='edit-product'),
    # Elimina el Producto con el Detalle de producto
    path('delete-product/<int:pk>/', viewsProductDetail.delete_product, name='delete_product'),

    
    # Trae toda la información de las tablas relacionadas con el producto
    #path('get-all-data_prod/', viewsGetAllDataProd.get_all_models_data, name='get_all_data'), 

    # Trae la información relacionada del producto con detalle de producto
    #path('get-all-detal_prod/', viewsGetAllDetaProd.get_all_datap, name='get_all_data'), 

    # ventas
    path('list-sales/', viewsSale.list_sale, name='list_sale'), # Listar 
    path('create-sales/', viewsSale.create_sale, name='create_sale'), # Crear
    path('update-sales/<int:pk>/', viewsSale.update_sale, name='update_sale'), # Editar
    path('delete-sales/<int:pk>/', viewsSale.delete_sale, name='delete_sale'), # Eliminar
    
    # Detalle ventas
    path('get-all-det_sales/', viewsDetailSale.get_all_datasale, name='get_all_data_sales'), # Listar en un EndPoint
    path('create-detail_sales/', viewsDetailSale.create_detail_sale, name='create_detail_sale'), # Crear
    path('update-detail_sales/<int:pk>/', viewsDetailSale.update_detail_sale, name='update_detail_sale'), # Editar
    path('delete-detail_sales/<int:pk>/', viewsDetailSale.delete_detail_sale, name='delete_detail_sale'), # Eliminar

    # Trae la información relacionada de la venta con detalle de la venta
    #path('get-all-det_sales/', viewsGetAllDetSale.get_all_datasale, name='get_all_data_sales'), 

    #  **RECUPERAR CONTRASEÑA**
    path('recup_contrasena/', viewsRecupContrasena.recuperar_contrasena, name='recuperar_contrasena'), #  
    path('cambiar_contrasena/<str:uidb64>/<str:token>/', viewsRecupContrasena.cambiar_contrasena, name='cambiar_contrasena'), #  

    # **Token**
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # link Ingreso usuario, para generar token
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
