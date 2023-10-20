from django.views import generic
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Atractivo, Parada, Recorrido, ParadaxRecorrido

# Create your views here.

def loginenter(request):
    return render(request, 'login.html')

def vista_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                # Superusuario, redirige al sitio de administración
                login(request,user)
                return redirect('admin:index')#HACER QUE SE LOGUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            if user.is_staff:
                # Chofer, redirige a tu vista personalizada
                login(request,user)
                return redirect('recorridos')
        else:
            # Lógica para manejar inicio de sesión fallido
            return render(request, 'error')


def index(request):
    return render(request, 'index.html')

def hopOnHopOff(request):
    return render(request, 'hopOnHopOff.html')

class RecorridosListView(generic.ListView):
    model = Recorrido
    context_object_name = 'recorrido_list'   # your own name for the list as a template variable
    queryset = Recorrido.objects.all() # Get 5 books containing the title war
    template_name = 'recorridos.html'
        

class ParadasDetailViews(generic.DetailView):
    model = Parada
    template_name = 'parada_detail.html'
    
class AtractivoDetailViews(generic.DetailView):
    model = Atractivo
    template_name = 'atractivo_detail.html'


def paradas_por_recorrido(request):
    #ANALIZAR ESTO PARA QUE NO SE PUEDAN REPETIR LOS NUMEROS DE PARADA EN EL ORDEN
    if request.method == 'POST':
        nombre_recorrido = request.POST.get('nombre_recorrido')
        paradas_del_recorrido = ParadaxRecorrido.objects.filter(recorrido__nombre=nombre_recorrido).order_by('nroParada')
        return render(request, 'paradas_por_recorrido.html', {'paradas_del_recorrido': paradas_del_recorrido})
    else:
        return render(request, 'index.html')
    

#@login_required
def cargaRecorridos(request):
    return render(request, 'cargaRecorridos.html')
