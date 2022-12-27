# Generated by Django 4.0.8 on 2022-12-27 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area_comun', '0002_reservaareacomun'),
        ('receipt', '0005_alter_receipt_receipt_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservation_receipt', to='area_comun.reservaareacomun', verbose_name='Reserva'),
        ),
    ]