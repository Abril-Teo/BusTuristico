from datetime import date, datetime
from django import forms
from .models import CambioEstado, Estado, Recorrido, Bus, Chofer
from django.contrib.auth.models import User

def validate_numeric(value):
    if not value.isdigit():
        raise forms.ValidationError('Este campo solo debe contener números.')

class NuevoViaje(forms.Form):
    nroViaje = forms.IntegerField()
    fecha = forms.DateField(initial=date.today())
    inicioEstimado = forms.TimeField(help_text="Ingresar el horario de inicio estimado")
    finalEstimado = forms.TimeField(help_text="Ingresar el horario de final estimado")
    chofer = forms.ModelChoiceField(queryset=Chofer.objects.all())
    bus = forms.ModelChoiceField(queryset=Bus.objects.all())
    recorrido = forms.ModelChoiceField(queryset=Recorrido.objects.all())
    
class NuevoChofer(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    legajo = forms.CharField(max_length=100)
    dni = forms.CharField(max_length=8, validators=[validate_numeric])
    def save_model(self, obj):
        username = obj.dni
        password = obj.legajo
        name = obj.nombre
        lastname = obj.apellido
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.first_name = name
        user.last_name = lastname
        user.is_staff = True
        user.save()
        obj.save()
        
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
    
