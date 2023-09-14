from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Models.controllers import viewsRol, viewsCategory , viewsPeople, viewsProduct, viewsState, viewsTypeProd, viewsProductDetail, viewsUser
from Models.controllers import viewsSale, viewsUserAllData, viewsMeasures, viewsMaterial, viewsCartItem
from Models.controllers import viewsRecupContrasena 
from Models.controllers import viewsReports
from Models import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse

urlpatterns = [

    # **Iniciar Sesion**
    path('login/', views.login, name='login'),
    # **Cerrar Sesion**
    path('log_out/', views.log_out, name='log_out'),

    #  **RECUPERAR CONTRASEÑA**
    path('recover_password/', viewsRecupContrasena.recover_password, name='recover_password'),

    # **Cambiar la contraseña**
    path('change_password/<str:uidb64>/<str:token>/', viewsRecupContrasena.change_password, name='change_password'), 

    # **Token**
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # link Ingreso usuario, para generar token
    # path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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
    path('create-people/', viewsPeople.create_people_and_user, name='create_people'), 
    # Editar People
    path('update-people/<int:pk>/', viewsPeople.update_people, name='update_people'),
    # Eliminar People
    path('delete-people/<int:pk>/', viewsPeople.delete_people, name='delete_people'),

    # ** Usuarios **

    # Listar Usuario
    path('list-user/', viewsUser.list_user, name='list_user'), 
    # Editar Usuario
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'), 
    # Eliminar Usuario
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'), 

    # Trae toda la información de las tablas relacionadas con el usuario 
    path('all_data_user/', viewsUserAllData.all_data_user, name='all_data_user'),

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

    # ** Medidas **
    # Listar Medidas
    path('list-measures/', viewsMeasures.list_measures, name='list-measures'), 
    # Crear Medidas
    path('create-measures/', viewsMeasures.create_measures, name='create-measures'),
    # Editar Medidas
    path('update-measures/<int:pk>/', viewsMeasures.update_measures, name='update-measures'), 
    # Eliminar Medidas
    path('delete-measures/<int:pk>/', viewsMeasures.delete_measures, name='delete-measures'),

    # ** Material **
    # Listar Material
    path('list-material/', viewsMaterial.list_material, name='list-material'), 
    # Crear Material
    path('create-material/', viewsMaterial.create_material, name='create_material'),
    # Editar Material
    path('update-material/<int:pk>/', viewsMaterial.update_material, name='update-material'), 
    # Eliminar Material
    path('delete-material/<int:pk>/', viewsMaterial.delete_material, name='delete-material'),

    # ** Productos **
    # Listar todos los modelos relacionados con Producto
    path('get-Product/', viewsProduct.get_Product, name='Estado-categ-tipo-producto'), 
    # Lista todo el producto completo con el Detalle Producto
    path('get-all-Product/', viewsProduct.get_all_Product, name='Estado-categ-tipo-producto-detalleProducto'),
    # http://localhost:8000/get_all_Product/?category_id=1&sort_by=price_sale  **Filtrar por la categoría con ID 1 y ordenar por precio de venta de forma ascendente**
    # http://localhost:8000/get_all_Product/?category_id=1&type_prod_id=2   **Filtrar por categoría y tipo de producto**
    # http://localhost:8000/get_all_Product/?min_price=50&max_price=100   **Filtrar por rango de precio mínimo y máximo**
    # http://localhost:8000/get_all_Product/?category_id=1&sort_by=-price_sale   **Filtrar por categoría, ordenar por precio de venta en orden descendente**
    # http://localhost:8000/get_all_Product/?type_prod_id=2&sort_by=name    **Filtrar por tipo de producto, ordenar por nombre de producto en orden ascendente**


    # ** Producto con Detalle Producto **
    # Crea el Producto con el Detalle de Producto
    path('create-product/', viewsProductDetail.product_create, name='crear_producto_detalle_product'),
    # lista el Producto con Detalle Producto y Estado
    path('list-product/', viewsProductDetail.product_details, name='product-details'),
    # Edita el Producto con el Detalle de Producto
    path('update-product/<int:product_id>/', viewsProductDetail.edit_product, name='edit-product'),
    # Elimina el Producto con el Detalle de producto
    path('delete-product/<int:pk>/', viewsProductDetail.delete_product, name='delete_product'),

    # ** Carrito y Cart_item **
    # Crear y Añadir un producto al carrito
    path('add_to_cart/', viewsCartItem.add_to_cart, name='add_to_cart'),
    # Actualizar la cantidad de un producto en el carrito
    path('remove_cart_item/', viewsCartItem.remove_product_from_cart, name='remove_cart_item'),
    # Disminuir la cantidad de un producto
    path('decrease_cart_item/', viewsCartItem.decrease_product_quantity, name='decrease_cart_item'),
    # Ver el contenido del carrito con detalles de productos
    path('list_cart/<int:user_id>/', viewsCartItem.list_cart, name='list_cart'),
    # Vaciar completamente el carrito
    path('clear_cart/<int:user_id>/', viewsCartItem.clear_cart, name='clear_cart'), 

    # ** Venta con Detalle Venta **
    # Crea la venta con el detalle de venta
    path('create-sale-detail/', viewsSale.create_sale_detail, name='create-sale-detail'),
    # Lista la venta con el detalle de venta
    path('list_sale_detail/', viewsSale.list_sale_detail, name='list_sale_detail'),
    # Edita la venta con el detalle de venta
    path('edit-sale-detail/<int:pk>/', viewsSale.edit_sale_detail, name='edit_sale_detail'),
    # Elimina la venta con el detalle de venta
    path('delete-sale-detail/<int:pk>/', viewsSale.delete_sale_detail, name='delete_sale_detail'),
    
    # Reports
    path('sales_report/', viewsReports.sales_report, name='sales_report'),  
    path('generate_product_sales_report/', viewsReports.generate_product_sales_report, name='generate_product_sales_report'), 
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
