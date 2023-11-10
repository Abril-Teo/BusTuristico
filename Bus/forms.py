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
    def get_nro_viaje_initial():
        return Viaje.objects.count() + 1

    nroViaje = forms.IntegerField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        initial=get_nro_viaje_initial(),
    )
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
"""class MostrarRecorridos(forms.Form):

    def __init__(self, *args, **kwargs):
        viaje_id = kwargs.pop('viaje_id', None)
        super(MostrarRecorridos, self).__init__(*args, **kwargs)
        
        if viaje_id is not None:
            viaje = Viaje.objects.get(nro_viaje=viaje_id)
            
            self.fields['fecha'] = forms.DateField(
                initial=viaje.fecha,
                error_messages={'required': 'Este campo es obligatorio.'}
            )
            
            self.fields['inicioEstimado'] = forms.TimeField(
                initial=viaje.inicio_estimado,
                help_text="Ingresar el horario de inicio estimado",
                error_messages={'required': 'Este campo es obligatorio.'}
            )
            
            self.fields['finalEstimado'] = forms.TimeField(
                initial=viaje.final_estimado,
                help_text="Ingresar el horario de final estimado",
                error_messages={'required': 'Este campo es obligatorio.'}
            )
       
    nroViaje = forms.IntegerField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        #initial=get_nro_viaje_initial(),
    )
    fecha = forms.DateField(
        #initial=Viaje.objects.get(nro_viaje = viaje_id).fecha,
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    inicioEstimado = forms.TimeField(
        #initial=get_lastest_inicio_estimado(),
        help_text="Ingresar el horario de inicio estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    finalEstimado = forms.TimeField(
      #  initial=get_lastest_final_estimado(),
        help_text="Ingresar el horario de final estimado",
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    
    inicio_time = Viaje.objects.last().inicio_estimado
    final_time = Viaje.objects.last().final_estimado

    # Calcula la diferencia en minutos sin tener en cuenta los segundos restantes
    duracion_viaje = (final_time.hour - inicio_time.hour) * 60 + (final_time.minute - inicio_time.minute)


    recorrido = forms.ModelChoiceField(
        queryset=Recorrido.objects.filter(duracionAprox__gte=duracion_viaje),
        help_text="",
        widget=forms.RadioSelect(),
        empty_label=None,
        error_messages={'required': 'Este campo es obligatorio.'}
    )

    def init(self, args, **kwargs):
        duracion = kwargs.pop('duracion', None)  # Obtiene el valor de 'duracion' pasado como parámetro

        super(MostrarRecorridos, self).init(args, **kwargs)

        if duracion is not None:
            self.fields['recorrido'].queryset = Recorrido.objects.filter(duracionAprox=duracion)

"""
class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['nro_viaje', 'fecha', 'inicio_real', 'final_real', 'inicio_estimado', 'final_estimado', 'chofer', 'bus', 'recorrido']
    
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
