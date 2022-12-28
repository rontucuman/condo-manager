import datetime

from area_comun.models import AreaComun, ReservaAreaComun
from django.conf import settings
from django.db import models

YESNO_CHOICES = (
    (True, 'Si'),
    (False, 'No')
)
# Create your models here.


class Receipt(models.Model):
    receipt_number = models.PositiveIntegerField(verbose_name='Recibo No.', unique=True)
    registered_date = models.DateTimeField(verbose_name='Fecha de Pago')
    reservation_amount = models.DecimalField(verbose_name='Monto de Reserva', decimal_places=2, max_digits=10,
                                             default=0)
    paid_amount = models.DecimalField(verbose_name='Monto Pagado', decimal_places=2, max_digits=10, default=0)
    is_canceled = models.BooleanField(verbose_name='Cancelado?', choices=YESNO_CHOICES, default=False)
    begin_reservation_date = models.DateTimeField(verbose_name='Inicio de Reserva', blank=True, null=True)
    end_reservation_date = models.DateTimeField(verbose_name='Fin de Reserva', blank=True, null=True)
    is_reservation_confirmed = models.BooleanField(verbose_name='Reserva Confirmada?', choices=YESNO_CHOICES,
                                                   default=False)
    is_reservation_canceled = models.BooleanField(verbose_name='Reserva Cancelada?', choices=YESNO_CHOICES,
                                                  default=False)
    # filepath = models.FilePathField(max_length=500, verbose_name='Ubicacion del Recibo', blank=True, null=True)
    filename = models.CharField(max_length=48, blank=True, null=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='user_receipt',
        blank=True,
        null=True
    )
    common_area = models.ForeignKey(
        to=AreaComun,
        on_delete=models.SET_NULL,
        verbose_name='Area Comun',
        related_name='commonarea_receipt',
        blank=True,
        null=True
    )
    reservation = models.ForeignKey(
        to=ReservaAreaComun,
        on_delete=models.SET_NULL,
        verbose_name='Reserva',
        related_name='reservation_receipt',
        blank=True,
        null=True
    )
