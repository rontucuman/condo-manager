from django.db import models

# Create your models here.

class AreaComun(models.Model):
    nombre = models.CharField(max_length=25, null=False, unique=True)
    descripcion = models.TextField(max_length=100)
    mobiliario = models.TextField(max_length=100, default='Ninguno')
    costo = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"id:{self.id} nombre:{self.nombre}"