from django.db import models

# Create your models here.

from django.db import models

# Create your models here.


    
class Estado(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    
    
class Bus(models.Model):
    patente = models.CharField(max_length=12)
    numUnidad = models.IntegerField()
    fechaCompra = models.DateField()
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    
    
class CambioEstado(models.Model):
    fechaCambio = models.DateTimeField(auto_now=True)
    estadoAnterior = models.ForeignKey('Estado', related_name='estadoAnterior',on_delete=models.CASCADE)
    estadoNuevo = models.ForeignKey('Estado', related_name='estadoNuevo', on_delete=models.CASCADE)
    bus = models.ForeignKey('Bus',on_delete=models.CASCADE)