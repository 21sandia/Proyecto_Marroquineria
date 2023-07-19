from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

from Models.controllers import viewsRole, viewsCategory , viewsProduct, viewsState, viewsTypeProd, viewsDetailProd, viewsUser
from Models.controllers import viewsSale, viewsDetailSale, viewsGroup
from Models.controllers import viewsRecupContrasena
from django.contrib.auth.models import Group
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('list-state/', viewsState.list_Status_g, name='list_state'), # Listar 
    path('create-state/', viewsState.create_Status_g, name='create_state'), # Crear
    path('update-state/<int:pk>/', viewsState.update_Status_g, name='update_state'), # Editar
    path('delete-state/<int:pk>/', viewsState.delete_Status_g, name='delete_state'), # Eliminar

    path('list-roles/', viewsRole.list_role, name='list_role'), # Listar
    path('create-roles/', viewsRole.create_role, name='create_role'), # Crear
    path('update-roles/<int:pk>/', viewsRole.update_role, name='update_role'), # Editar
    path('delete-roles/<int:pk>/', viewsRole.delete_role, name='delete_role'), # Eliminar

    path('list-group/', viewsGroup.list_group, name='list_group'), # Listar
    
    path('list-category/', viewsCategory.list_category, name='list_category'), # Listar
    path('create-category/', viewsCategory.create_category, name='create_category'), # Crear
    path('update-category/<int:pk>/', viewsCategory.update_category, name='update_category'), # Editar
    path('delete-category/<int:pk>/', viewsCategory.delete_category, name='delete_category'), # Eliminar

    path('list-type_prod/', viewsTypeProd.list_type_prod, name='list_type_prod'), # Listar
    path('create-type_prod/', viewsTypeProd.create_type_prod, name='create_type_prod'), # Crear
    path('update-type_prod/<int:pk>/', viewsTypeProd.update_type_prod, name='update_type_prod'), # Editar
    path('delete-type_prod/<int:pk>/', viewsTypeProd.delete_type_prod, name='delete_type_prod'), # Eliminar

    path('list-products/', viewsProduct.list_product, name='list_product'), # Listar
    path('create-products/', viewsProduct.create_product, name='create_product'), # Crear
    path('update-products/<int:pk>/', viewsProduct.update_product, name='update_product'), # Editar
    path('delete-products/<int:pk>/', viewsProduct.delete_product, name='delete_product'), # Eliminar
    
    path('list-detail_prod/', viewsDetailProd.list_detailProd, name='list_detail_prod'), # Listar
    path('create-detail_prod/', viewsDetailProd.create_detailProd, name='create_detail_prod'), # Crear
    path('update-detail_prod/<int:pk>/', viewsDetailProd.update_detailProd, name='update_detail_prod'), # Editar
    path('delete-detail_prod/<int:pk>/', viewsDetailProd.delete_detailProd, name='delete_detail_prod'), # Eliminar

    path('list-sales/', viewsSale.list_sale, name='list_sale'), # Listar 
    path('create-sales/', viewsSale.create_sale, name='create_sale'), # Crear
    path('update-sales/<int:pk>/', viewsSale.update_sale, name='update_sale'), # Editar
    path('delete-sales/<int:pk>/', viewsSale.delete_sale, name='delete_sale'), # Eliminar
    
    path('list-detail_sales/', viewsDetailSale.list_detail_sale, name='list_detail_sale'), # Listar 
    path('create-detail_sales/', viewsDetailSale.create_detail_sale, name='create_detail_sale'), # Crear
    path('update-detail_sales/<int:pk>/', viewsDetailSale.update_detail_sale, name='update_detail_sale'), # Editar
    path('delete-detail_sales/<int:pk>/', viewsDetailSale.delete_detail_sale, name='delete_detail_sale'), # Eliminar

    path('list-user/', viewsUser.list_user, name='list_user'), # Listar 
    path('create-user/', viewsUser.create_user, name='create_user'), # Crear
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'), # Editar
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'), # Eliminar

    #  **RECUPERAR CONTRASEÑA**
    path('recup_contrasena/', viewsRecupContrasena.recuperar_contrasena, name='recuperar_contrasena'), #  
    path('cambiar_contrasena/<str:uidb64>/<str:token>/', viewsRecupContrasena.cambiar_contrasena, name='cambiar_contrasena'), #  

    # **Token**
    path('api-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # link Ingreso usuario, para generar token
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
