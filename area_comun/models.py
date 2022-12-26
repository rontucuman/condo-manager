from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.

class AreaComun(models.Model):
    nombre = models.CharField(max_length=25, null=False, unique=True)
    descripcion = models.TextField(max_length=100)
    mobiliario = models.TextField(max_length=100, default='Ninguno')
    costo = models.PositiveIntegerField(default=0)
    # Actualmente solo soportamos una cuenta de administrador entonces no necesitamos la siguiente relacion por el momento
    # administrador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"id:{self.id} nombre:{self.nombre}"

class ReservaAreaComun(models.Model):
    area_comun = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="disponibilidadDeAreaComun")
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="misReservas")
    fecha = models.DateField()
    confirmada = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"id:{self.id} area_comun:{self.area_comun} propietario:{self.propietario} fecha:{self.fecha}"

    class Meta:
        unique_together = [['area_comun', 'fecha']]
