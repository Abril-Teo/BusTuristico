from datetime import date
from django.views import View, generic
from django.views.generic import DetailView, UpdateView
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required,user_passes_test
from .forms import NuevoViaje
from .models import Bus, Viaje
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone



from .models import Atractivo, Parada, Recorrido, ParadaxRecorrido

def vista_login(request):
    return render(request, 'login.html')

def logincomprobacion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('solosuper')
            if user.is_staff:
                login(request, user)
                return HttpResponseRedirect('/bus/staff/')

            #  ....
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})


def index(request):
    return render(request, 'index.html')

def hopOnHopOff(request):
    return render(request, 'hopOnHopOff.html')

class RecorridosListView(generic.ListView):
    model = Recorrido
    context_object_name = 'recorrido_list' 
    queryset = Recorrido.objects.all() 
    template_name = 'recorridos.html'
        

class ParadasDetailViews(generic.DetailView):
    model = Parada
    template_name = 'parada_detail.html'
    
class AtractivoDetailViews(generic.DetailView):
    model = Atractivo
    template_name = 'atractivo_detail.html'

class CargarViajeDetailViews(UpdateView, DetailView):
    model = Viaje
    template_name = 'cargar_viaje.html'
    fields = ['inicio_real', 'final_real']


def paradas_por_recorrido(request):
    if request.method == 'POST':
        nombre_recorrido = request.POST.get('nombre_recorrido')
        paradas_del_recorrido = ParadaxRecorrido.objects.filter(recorrido__nombre=nombre_recorrido).order_by('nroParada')
        return render(request, 'paradas_por_recorrido.html', {'paradas_del_recorrido': paradas_del_recorrido})
    else:
        return render(request, 'index.html')
    
def cerrar_sesion(request):
    logout(request)
    return redirect('index') 
@login_required
def cargaRecorridos(request):
    return render(request, 'cargaRecorridos.html')

@user_passes_test(lambda u: u.is_superuser)
def superuseronly(request):
    return render(request, 'solosuper.html')

@user_passes_test(lambda u: u.is_staff)
def staffonly(request):
    if request.method == 'POST':
        dni_chofer = request.user.username
        viajes_del_chofer = Viaje.objects.filter(chofer__dni=dni_chofer).filter(fecha=date.today()).order_by('inicio_estimado')
        return render(request, 'solostaff.html', {'viajes_choffer': viajes_del_chofer})
    else:
        return render(request, 'index.html')
    #return render(request, 'solostaff.html')


def viewViaje(request):
    if request.method == 'POST':
        formulario = NuevoViaje(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Viaje(nro_viaje=datos_formulario['nroViaje'] ,fecha=datos_formulario['fecha'], inicio_estimado=datos_formulario['inicioEstimado'], final_estimado=datos_formulario['finalEstimado'], chofer=datos_formulario['chofer'], bus=datos_formulario['bus'],recorrido=datos_formulario['recorrido'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})