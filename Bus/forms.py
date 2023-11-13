from datetime import date, datetime, timedelta
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.safestring import mark_safe

def validate_numeric(value):
    if not value.isdigit():
        raise forms.ValidationError('Este campo solo debe contener números.')



class NuevoViaje(forms.Form):

    nroViaje = forms.IntegerField(
        label='Número de Viaje', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    def __init__(self, *args, **kwargs):
        super(NuevoViaje, self).__init__(*args, **kwargs)
        self.fields['nroViaje'].initial = Viaje.obtener_proximo_nro_viaje()
        #BASICAMENTE CADA VEZ QUE SE RENDERIZA EL FORMULARIO SE GENERA UN NUEVO NUMERO DE VIAJE PORQUE SI LO PONGO ADENTRO DE EL CAMPO SE CREA 1 SOLA VEZ Y NO SE ACTUALIZA
    fecha = forms.DateField(
        initial=date.today().strftime('%Y-%m-%d'),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    inicioEstimado = forms.TimeField(
        help_text="Ingresar el horario de inicio estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    finalEstimado = forms.TimeField(
        help_text="Ingresar el horario de final estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['nro_viaje', 'fecha', 'inicio_estimado', 'final_estimado', 'chofer', 'bus', 'recorrido']
    
class NuevoChofer(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    legajo = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=8, validators=[validate_numeric])
    
    
        
        
class NuevoBus(forms.Form):
    patente = forms.CharField(max_length=12)
    numUnidad = forms.IntegerField()
    fechaCompra = forms.DateField()
    estado = forms.ModelChoiceField(queryset=CambioEstado.objects.all())

class NuevoRecorrido(forms.Form):
    nombre = forms.CharField(max_length=100)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), initial='#FF0000')
    duracionAprox = forms.IntegerField()
    horaInicioAprox = forms.TimeField(help_text="Ingresar el horario de inicio estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    horaFinalizacionAprox = forms.TimeField(help_text="Ingresar el horario de Finalizacion estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    frecuencia = forms.IntegerField()

class AgregarParada(forms.Form):
    nroParada = forms.IntegerField()
    llegadaEstimada = forms.TimeField(help_text="Ingresar el horario de llegada estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    recorrido = forms.ModelChoiceField(queryset=Recorrido.objects.all(),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    parada = forms.ModelChoiceField(queryset=Parada.objects.all(),
        error_messages={'required': 'Este campo es obligatorio.'}
    )

class NuevaParada(forms.Form):
    nombre = forms.CharField(max_length=100)
    calle = forms.CharField(max_length=100)
    numero = forms.IntegerField()
    decripcion = forms.CharField(max_length=200)
    foto = forms.CharField(max_length=200)
    atractivos = forms.ModelMultipleChoiceField(
        queryset=Atractivo.objects.all(),  # Debes definir la queryset para los objetos Atractivo disponibles
        widget=forms.CheckboxSelectMultiple,  # Puedes usar CheckboxSelectMultiple u otro widget adecuado
        required=False,  # Si no es requerido, establece esto en False
    )
"""
class NuevoCambioEstado(forms.Form):
    fechaCambio = forms.DateField(initial=datetime.today(), widget=forms.DateInput(attrs={'disabled': 'disabled'}))#si no anda cambiar a date el datetime
    estadoAnterior = forms.ModelChoiceField(queryset=Estado.objects.all())
    estadoNuevo = forms.ModelChoiceField(queryset=Estado.objects.all())
    motivo = forms.CharField(max_length=100)
    
class NuevoEstado(forms.Form):
    nombre = forms.CharField(max_length=100)
    habilitado = forms.BooleanField()
    detalles = forms.CharField(max_length=250)
""" 
