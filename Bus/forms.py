from datetime import date, datetime
from django import forms
from .models import CambioEstado, Estado, Recorrido, Bus, Chofer
from django.contrib.auth.models import User

def validate_numeric(value):
    if not value.isdigit():
        raise forms.ValidationError('Este campo solo debe contener números.')

class NuevoViaje(forms.Form):
    nroViaje = forms.IntegerField(
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    fecha = forms.DateField(initial=date.today(),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    inicioEstimado = forms.TimeField(help_text="Ingresar el horario de inicio estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    finalEstimado = forms.TimeField(help_text="Ingresar el horario de final estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    chofer = forms.ModelChoiceField(queryset=Chofer.objects.all(),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    bus = forms.ModelChoiceField(queryset=Bus.objects.filter(estado__estadoNuevo__habilitado = True),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    recorrido = forms.ModelChoiceField(queryset=Recorrido.objects.all(),
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    
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
    
class NuevoCambioEstado(forms.Form):
    fechaCambio = forms.DateField(initial=datetime.today(), widget=forms.DateInput(attrs={'disabled': 'disabled'}))#si no anda cambiar a date el datetime
    estadoAnterior = forms.ModelChoiceField(queryset=Estado.objects.all())
    estadoNuevo = forms.ModelChoiceField(queryset=Estado.objects.all())
    motivo = forms.CharField(max_length=100)
    
class NuevoEstado(forms.Form):
    nombre = forms.CharField(max_length=100)
    habilitado = forms.BooleanField()
    detalles = forms.CharField(max_length=250)
    
