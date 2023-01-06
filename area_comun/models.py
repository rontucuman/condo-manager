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
    fecha_registro = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"id:{self.id} area_comun:{self.area_comun} propietario:{self.propietario} fecha:{self.fecha}"

    @property
    def dias_faltantes_eliminar_reserva(self):
        fecha_actual = datetime.now().date()
        if fecha_actual == self.fecha_registro: 
            return 3
        return 3 - int(str(fecha_actual - self.fecha_registro).split(" ")[0])

    def save(self, *args, **kwargs):
        bitacora_ReservaAreaComun(
            area_comun=self.area_comun, 
            propietario=self.propietario, 
            fecha=self.fecha, 
            confirmada=self.confirmada, 
            fecha_registro=self.fecha_registro,
            evento="Creado").save()
        return super().save(*args, **kwargs)
         
    class Meta:
        unique_together = [['area_comun', 'fecha']]
    
class bitacora_ReservaAreaComun(models.Model):
    area_comun = models.ForeignKey(AreaComun, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    confirmada = models.BooleanField(default=False)
    fecha_registro = models.DateField(auto_now=True)
    evento = models.TextField()