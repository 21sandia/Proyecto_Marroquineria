from django.urls import path, include
from rest_framework import routers
from . import views

from Models.users.views import Login

router = routers.DefaultRouter()  # Permite manejar multiples rutas
router.register(r'Role', views.RoleViewSet, 'Role')
router.register(r'People', views.PeopleViewSet, 'People')  
router.register(r'Category', views.CategoryViewSet,'category')  
router.register(r'Type_prod', views.Type_prodViewSet, 'Type_prod') 
router.register(r'Product', views.ProductViewSet, 'Product')
router.register(r'Order', views.OrderViewSet, 'Order') 
router.register(r'Carts', views.CartsViewSet, 'Carts') 
router.register(r'Detail_sale', views.Detail_saleViewSet, 'Detail_sale') 

urlpatterns = [
    path('api/', include(router.urls)),
    path('', Login.as_view(), name = 'Login'),
]

