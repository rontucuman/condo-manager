# Generated by Django 4.0.8 on 2023-01-13 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area_comun', '0002_reservaareacomun'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservaareacomun',
            name='fecha_registro',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='bitacora_ReservaAreaComun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('confirmada', models.BooleanField(default=False)),
                ('fecha_registro', models.DateField(auto_now=True)),
                ('evento', models.TextField()),
                ('area_comun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area_comun.areacomun')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
