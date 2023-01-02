from django.urls import path
from . import views


urlpatterns = [
    # path('list-reservations/', views.list_reservations, name='list_reservations'),
    # path('list-reservations1/', views.list_reservations1, name='list_reservations1'),
    path('list-reservations2/', views.list_reservations2, name='list_reservations2'),
    path('get-reservations-content/', views.get_reservations_content, name='get_reservations_content'),
    path('get-pagination-content/', views.get_pagination_content, name='get_pagination_content'),
    # path('list-reservations2/<str:page>/<str:numitems>', views.list_reservations2, name='list_reservations2'),
    path('process-confirm-reservation/', views.confirm_reservation, name='confirm_reservation'),
    path('process-cancel-reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('show-pdf/<str:doc>', views.show_pdf, name='show_pdf')
]
