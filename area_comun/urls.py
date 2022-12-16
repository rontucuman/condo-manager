
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import registrar_area_comun

urlpatterns = [
    path('registrar/', registrar_area_comun, name='registrar_area_comun'),
]
