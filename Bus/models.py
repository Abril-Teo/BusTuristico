from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from colorfield.fields import ColorField
import webcolors
from django.core.validators import FileExtensionValidator


# Create your models here.

from django.db import models

# Create your models here.


    
class Estado(models.Model):
    nombre = models.CharField(max_length=100)
    habilitado = models.BooleanField()
    detalles = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.nombre
    
class Viaje(models.Model):
    nro_viaje = models.IntegerField()
    fecha = models.DateField()
    inicio_real = models.TimeField()
    final_real = models.TimeField()
    inicio_estimado = models.TimeField()
    final_estimado = models.TimeField()
    chofer = models.ForeignKey('Chofer', on_delete=models.CASCADE)
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.nro_viaje

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
    
class Recorrido(models.Model):
    hex_color = ColorField(default= '#FF0000')
    duracionAprox = models.IntegerField("Duracion en minutos")
    horaInicioAprox = models.DateTimeField()
    horaFinalizacionAprox = models.DateTimeField()
    frecuencia = models.IntegerField()
    
    def __str__(self) -> str:
        color_name = webcolors.hex_to_name(self.hex_color)
        return color_name
    
    def obtenerParadas(self):
        return "metodo Obtener Paradas"
    def new(self):
        return "metodo New"

class Chofer(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    leagajo = models.CharField(max_length=100)
    dni = models.IntegerField()
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
    descripcion = models.CharField(max_length=150)
    foto = models.CharField(max_length=500)
    calificacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    
    def __str__(self) -> str:
        return self.nombre

class Parada(models.Model):
    nombre = models.CharField(max_length= 45)
    calle = models.CharField(max_length=45)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=255)
    foto = models.FileField(upload_to='imagenes/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    atractivos = models.ManyToManyField(Atractivo)
    
    def __str__(self) -> str:
        return self.nombre

class ParadaxRecorrido(models.Model):
    nroParada = models.IntegerField()
    llegadaEstimada = models.TimeField()
    recorrido = models.ForeignKey('Recorrido', on_delete=models.CASCADE)
    parada = models.ForeignKey('Parada', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.recorrido + " " + self.parada
    
    def DefinirOrdenParadas(): #ACA IRA UNA FUNCION EN LA QUE SE ORDENEN LAS PARADAS EN UN ARRAY POSIBLEMENTE
        pass 


    