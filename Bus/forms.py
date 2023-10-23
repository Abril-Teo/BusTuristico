from datetime import date
from django import forms
from .models import Recorrido, Bus, Chofer


class NuevoViaje(forms.Form):
    nroViaje = forms.IntegerField()
    fecha = forms.DateField(initial=date.today())
    inicioEstimado = forms.TimeField(help_text="Ingresar el horario de inicio estimado")
    finalEstimado = forms.TimeField(help_text="Ingresar el horario de final estimado")
    chofer = forms.ModelChoiceField(queryset=Chofer.objects.all())
    bus = forms.ModelChoiceField(queryset=Bus.objects.all())
    recorrido = forms.ModelChoiceField(queryset=Recorrido.objects.all())