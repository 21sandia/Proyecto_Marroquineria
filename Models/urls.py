from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()  # Permite manejar multiples rutas
router.register(r'models', views.ModelsViewSet)  # Asegúrate de que el nombre de la vista sea correcto

urlpatterns = [
    path('', include(router.urls)),
]

