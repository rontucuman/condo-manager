# Generated by Django 4.0.8 on 2022-12-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0004_alter_receipt_common_area_alter_receipt_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='receipt_number',
            field=models.PositiveIntegerField(unique=True, verbose_name='Recibo No.'),
        ),
    ]