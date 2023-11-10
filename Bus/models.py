from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

from django.forms import ValidationError
from colorfield.fields import ColorField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from django.db import models

def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError('Este campo solo debe contener números.')

class Estado(models.Model):
    nombre = models.CharField(max_length=100)
    habilitado = models.BooleanField()
    detalles = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.nombre
    
class Viaje(models.Model):
    
    nro_viaje = models.IntegerField()
    fecha = models.DateField()
    inicio_real = models.TimeField(null=True, blank=True)
    final_real = models.TimeField(null=True, blank=True)
    inicio_estimado = models.TimeField()
    final_estimado = models.TimeField()
    chofer = models.ForeignKey('Chofer', on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE, null=True, blank=True)
    recorrido = models.ForeignKey('Recorrido', on_delete=models.CASCADE, null=True, blank=True)

    
    
    

    def CalcularDemora(self):
        return self.inicio_real - self.inicio_estimado

    def ingresarInicio(self):
        self.inicio_real = datetime.time.now()
    
    def ingresarFin(self):
        self.final_real = datetime.time.now()
    
    def CalcularDuracionEstimada(self):
        return self.final_estimado - self.inicio_estimado


    def CalcularDuracionFinal(self):
        return self.final_real - self.inicio_real
    
    def generarInforme(self):
        pass

    def __str__(self) -> str:
        return str(self.nro_viaje)
    
class Recorrido(models.Model):
    nombre = models.CharField(max_length=50)
    hex_color = ColorField(default= '#FF0000')
    duracionAprox = models.IntegerField("Duracion en minutos")
    horaInicioAprox = models.TimeField()
    horaFinalizacionAprox = models.TimeField()
    frecuencia = models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.nombre}'
    
    def obtenerParadas(self):
        return "metodo Obtener Paradas"
    def new(self):
        return "metodo New"

class Chofer(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    legajo = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, validators=[validate_numeric])
    def __str__(self) -> str:
        return self.nombre + " " + self.apellido

class Bus(models.Model):
    patente = models.CharField(max_length=12)
    numUnidad = models.IntegerField()
    fechaCompra = models.DateField()
    estado = models.ForeignKey('CambioEstado', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.patente
    def isHabilitado(self):
        return self.estado.habilitado
    
    
class CambioEstado(models.Model):
    fechaCambio = models.DateTimeField(auto_now=True)
    estadoAnterior = models.ForeignKey('Estado', related_name='estadoAnterior',on_delete=models.CASCADE)
    estadoNuevo = models.ForeignKey('Estado', related_name='estadoNuevo', on_delete=models.CASCADE)
    motivo = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.estadoAnterior.nombre + " " + self.estadoNuevo.nombre

class Atractivo(models.Model):
    nombre = models.CharField(max_length= 45)
    calle = models.CharField(max_length=45)
    numero = models.IntegerField()
    descripcion = models.TextField()
    foto = models.FileField(upload_to='imagenes/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    calificacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self) -> str:
        return self.nombre
    
    def estrellas_vacias(self) -> int:
        estrellas_va = (5 - self.calificacion)
        return estrellas_va
    
    def get_range(value):
        return range(value)

class Parada(models.Model):
    nombre = models.CharField(max_length= 45)
    calle = models.CharField(max_length=45)
    numero = models.IntegerField()
    descripcion = models.TextField()
    foto = models.FileField(upload_to='imagenes/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    atractivos = models.ManyToManyField(Atractivo)
    
    def __str__(self) -> str:
        return self.nombre

class ParadaxRecorrido(models.Model):
    nroParada = models.IntegerField()#ACA VA EL ORDEN DE LA PARADA
    llegadaEstimada = models.TimeField()
    recorrido = models.ForeignKey('Recorrido', on_delete=models.CASCADE)
    parada = models.ForeignKey('Parada', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.recorrido.__str__() + " " + self.parada.__str__()
    
    def clean(self):
        if ParadaxRecorrido.objects.filter(recorrido=self.recorrido, nroParada=self.nroParada).exclude(pk=self.pk).exists():
            raise ValidationError('ESTA POSICION YA ESTA OCUPADA POR UNA PARADA SELECCIONE OTRA PORFAVOR.')
            
        
