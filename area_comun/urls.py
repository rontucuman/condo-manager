
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import registrar_area_comun, lista_areas_comunes, reservar_area_comun, mis_reservas_area_comun, ver_recibo, eliminar_reserva

urlpatterns = [
    path('registrar/', registrar_area_comun, name='registrar_area_comun'),
    path('lista/', lista_areas_comunes, name='lista_areas_comunes'),
    path('<int:area_comun_id>', reservar_area_comun, name='reservar_area_comun'),
    path('misReservas/', mis_reservas_area_comun, name='mis_reservas_area_comun'),
    path('ver-recibo/<int:reserva_id>', ver_recibo, name='ver_recibo'),
    path('eliminarReserva/<int:reserva_id>', eliminar_reserva, name='eliminar_reserva'),    
]
