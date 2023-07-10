from django.urls import path
from Models.controllers import viewsPeople, viewsRole, viewsCategory , viewsProduct, viewsState, viewsTypeProd, viewsDetailProd, viewsUser
from Models.controllers import viewsSale, viewsDetailSale

urlpatterns = [

    path('state/', viewsState.list_Status, name='list_state'),
    path('state/create/', viewsState.create_Status, name='create_state'),
    path('state/update/<int:pk>/', viewsState.update_Status, name='update_state'),
    path('state/delete/<int:pk>/', viewsState.delete_Status, name='delete_state'),

    path('roles/', viewsRole.list_role, name='list_role'),
    path('roles/create/', viewsRole.create_role, name='create_role'),
    path('roles/update/<int:pk>/', viewsRole.update_role, name='update_role'),
    path('roles/delete/<int:pk>/', viewsRole.delete_role, name='delete_role'),
    
    path('people/', viewsPeople.list_people, name='list_people'),
    path('people/create/', viewsPeople.create_people, name='create_people'),
    path('people/update/<int:pk>/', viewsPeople.update_people, name='update_people'),
    path('people/delete/<int:pk>/', viewsPeople.delete_people, name='delete_people'),
    
    path('category/', viewsCategory.list_category, name='list_category'),
    path('category/create/', viewsCategory.create_category, name='create_category'),
    path('category/update/<int:pk>/', viewsCategory.update_category, name='update_category'),
    path('category/delete/<int:pk>/', viewsCategory.delete_category, name='delete_category'),

    path('type_prod/', viewsTypeProd.list_type_prod, name='list_type_prod'),
    path('type_prod/create/', viewsTypeProd.create_type_prod, name='create_type_prod'),
    path('type_prod/update/<int:pk>/', viewsTypeProd.update_type_prod, name='update_type_prod'),
    path('type_prod/delete/<int:pk>/', viewsTypeProd.delete_type_prod, name='delete_type_prod'),

    path('products/', viewsProduct.list_product, name='list_product'),
    path('products/create/', viewsProduct.create_product, name='create_product'),
    path('products/update/<int:pk>/', viewsProduct.update_product, name='update_product'),
    path('products/delete/<int:pk>/', viewsProduct.delete_product, name='delete_product'),
    
    path('detail_prod/', viewsDetailProd.list_detailProd, name='list_detail_prod'),
    path('detail_prod/create/', viewsDetailProd.create_detailProd, name='create_detail_prod'),
    path('detail_prod/update/<int:pk>/', viewsDetailProd.update_detailProd, name='update_detail_prod'),
    path('detail_prod/delete/<int:pk>/', viewsDetailProd.delete_detailProd, name='delete_detail_prod'),

    path('sales/', viewsSale.list_sale, name='list_sale'),
    path('sales/create/', viewsSale.create_sale, name='create_sale'),
    path('sales/update/<int:pk>/', viewsSale.update_sale, name='update_sale'),
    path('sales/delete/<int:pk>/', viewsSale.delete_sale, name='delete_sale'),
    
    path('detail_sales/', viewsDetailSale.list_detail_sale, name='list_detail_sale'),
    path('detail_sales/create/', viewsDetailSale.create_detail_sale, name='create_detail_sale'),
    path('detail_sales/update/<int:pk>/', viewsDetailSale.update_detail_sale, name='update_detail_sale'),
    path('detail_sales/delete/<int:pk>/', viewsDetailSale.delete_detail_sale, name='delete_detail_sale'),

    path('list-user/', viewsUser.list_user, name='list_user'),
    path('create-user/', viewsUser.create_user, name='create_user'),
    path('update-user/<int:pk>/', viewsUser.update_user, name='update_user'),
    path('delete-user/<int:pk>/', viewsUser.delete_user, name='delete_user'),
    
]
