from django.urls import path
from . import views


urlpatterns = [
    path('list-reservations/', views.list_reservations, name='list_reservations'),
    path('process-confirm-reservation/', views.confirm_reservation, name='confirm_reservation'),
    path('process-cancel-reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('show-pdf/<int:pdf_id>', views.show_pdf, name='show_pdf')
]