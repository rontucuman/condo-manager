# Generated by Django 4.0.8 on 2022-12-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_number', models.PositiveIntegerField(verbose_name='Recibo No.')),
                ('registered_date', models.DateTimeField(verbose_name='Fecha')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('is_canceled', models.BooleanField(choices=[(True, 'Si'), (False, 'No')], default=False, verbose_name='Cancelado?')),
            ],
        ),
    ]