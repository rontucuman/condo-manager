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
    registered_date = models.DateTimeField(verbose_name='Fecha')
    amount = models.DecimalField(verbose_name='Monto', decimal_places=2, max_digits=10)
    is_canceled = models.BooleanField(verbose_name='Cancelado?', choices=YESNO_CHOICES, default=False)
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
