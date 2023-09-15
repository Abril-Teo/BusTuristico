from django.shortcuts import render, redirect
from .models import Bus, Viaje
from .forms import NuevoViaje
# Create your views here.

def index(request):
    buses = Bus.objects.all()
    return render(request, 'index.html',{'buses': buses})

# En miapp/views.py

def viewRecorrido(request):
    if request.method == 'POST':
        formulario = NuevoViaje(request.POST)
        if formulario.is_valid():
            # Procesar los datos del formulario y guardarlos en el modelo
            datos_formulario = formulario.cleaned_data
            #nuevo_objeto = Recorrido(nombre=datos_formulario['nombre'], edad=datos_formulario['edad'], email=datos_formulario['email'])
            nuevo_objeto = Viaje(nro_viaje=datos_formulario['nroViaje'] ,fecha=datos_formulario['fecha'] ,inicio_real=datos_formulario['inicioReal'], final_real=datos_formulario['finalReal'], inicio_estimado=datos_formulario['inicioEstimado'], final_estimado=datos_formulario['finalEstimado'], chofer=datos_formulario['chofer'], bus=datos_formulario['bus'])
            nuevo_objeto.save()
            # Redirigir a una página de éxito o hacer cualquier otra cosa
            return redirect('http://127.0.0.1:8000/bus/')
    else:
        formulario = NuevoViaje()
    
    return render(request, 'templateViaje.html', {'formulario': formulario})
