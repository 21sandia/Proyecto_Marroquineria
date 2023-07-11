from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from Models.controllers import viewsPeople, viewsRole, viewsCategory , viewsProduct, viewsState, viewsTypeProd, viewsDetailProd, viewsUser
from Models.controllers import viewsSale, viewsDetailSale

urlpatterns = [

    path('list-state/', viewsState.list_Status, name='list_state'), #
    path('create-state/', viewsState.create_Status, name='create_state'),
    path('update-state/<int:pk>/', viewsState.update_Status, name='update_state'),
    path('delete-state/<int:pk>/', viewsState.delete_Status, name='delete_state'),

    path('list-roles/', viewsRole.list_role, name='list_role'),
    path('create-roles/', viewsRole.create_role, name='create_role'),
    path('update-roles/<int:pk>/', viewsRole.update_role, name='update_role'),
    path('delete-roles/<int:pk>/', viewsRole.delete_role, name='delete_role'),
    
    path('list-people/', viewsPeople.list_people, name='list_people'),
    path('create-people/', viewsPeople.create_people, name='create_people'),
    path('update-people/<int:pk>/', viewsPeople.update_people, name='update_people'),
    path('delete-people/<int:pk>/', viewsPeople.delete_people, name='delete_people'),
    
    path('list-category/', viewsCategory.list_category, name='list_category'),
    path('create-category/', viewsCategory.create_category, name='create_category'),
    path('update-category/<int:pk>/', viewsCategory.update_category, name='update_category'),
    path('delete-category/<int:pk>/', viewsCategory.delete_category, name='delete_category'),

    path('list-type_prod/', viewsTypeProd.list_type_prod, name='list_type_prod'),
    path('create-type_prod/', viewsTypeProd.create_type_prod, name='create_type_prod'),
    path('update-type_prod/<int:pk>/', viewsTypeProd.update_type_prod, name='update_type_prod'),
    path('delete-type_prod/<int:pk>/', viewsTypeProd.delete_type_prod, name='delete_type_prod'),

    path('list-products/', viewsProduct.list_product, name='list_product'),
    path('create-products/', viewsProduct.create_product, name='create_product'),
    path('update-products/<int:pk>/', viewsProduct.update_product, name='update_product'),
    path('delete-products/<int:pk>/', viewsProduct.delete_product, name='delete_product'),
    
    path('list-detail_prod/', viewsDetailProd.list_detailProd, name='list_detail_prod'),
    path('create-detail_prod/', viewsDetailProd.create_detailProd, name='create_detail_prod'),
    path('update-detail_prod/<int:pk>/', viewsDetailProd.update_detailProd, name='update_detail_prod'),
    path('delete-detail_prod/<int:pk>/', viewsDetailProd.delete_detailProd, name='delete_detail_prod'),

    path('list-sales/', viewsSale.list_sale, name='list_sale'),
    path('create-sales/', viewsSale.create_sale, name='create_sale'),
    path('update-sales/<int:pk>/', viewsSale.update_sale, name='update_sale'),
    path('delete-sales/<int:pk>/', viewsSale.delete_sale, name='delete_sale'),
    
    path('list-detail_sales/', viewsDetailSale.list_detail_sale, name='list_detail_sale'),
    path('create-detail_sales/', viewsDetailSale.create_detail_sale, name='create_detail_sale'),
    path('update-detail_sales/<int:pk>/', viewsDetailSale.update_detail_sale, name='update_detail_sale'),
    path('delete-detail_sales/<int:pk>/', viewsDetailSale.delete_detail_sale, name='delete_detail_sale'),

    path('list-user/', viewsUser.list_user, name='list_user'),
    path('create-user/', viewsUser.create_user, name='create_user'),
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'),
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'),

    path('models-token-auth/', obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
