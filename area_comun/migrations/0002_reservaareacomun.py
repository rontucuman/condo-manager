# Generated by Django 4.0.8 on 2022-12-27 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area_comun', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaAreaComun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('confirmada', models.BooleanField(default=False)),
                ('area_comun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disponibilidadDeAreaComun', to='area_comun.areacomun')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='misReservas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('area_comun', 'fecha')},
            },
        ),
    ]
