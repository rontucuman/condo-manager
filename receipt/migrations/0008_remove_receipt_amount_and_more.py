# Generated by Django 4.0.8 on 2022-12-28 02:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0007_receipt_is_reservation_confirmed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='reservation_date',
        ),
        migrations.AddField(
            model_name='receipt',
            name='begin_reservation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 28, 2, 0, 13, 807229), verbose_name='Inicio de Reserva'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='end_reservation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 28, 2, 0, 13, 807229), verbose_name='Fin de Reserva'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='is_reservation_canceled',
            field=models.BooleanField(choices=[(True, 'Si'), (False, 'No')], default=False, verbose_name='Reserva Cancelada?'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='paid_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto Pagado'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='reservation_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto de Reserva'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='registered_date',
            field=models.DateTimeField(verbose_name='Fecha de Pago'),
        ),
    ]
