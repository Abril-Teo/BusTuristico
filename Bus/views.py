from django.views import generic
from django.shortcuts import render,get_object_or_404

from .models import Parada, Recorrido, ParadaxRecorrido

# Create your views here.

def index(request):
    return render(request, 'index.html')

class RecorridosListView(generic.ListView):
    model = Recorrido
    context_object_name = 'recorrido_list'   # your own name for the list as a template variable
    queryset = Recorrido.objects.all() # Get 5 books containing the title war
    template_name = 'recorridos.html'
        

class ParadasDetailViews(generic.DetailView):
    model = Parada
    template_name = 'parada_detail.html'
    
class AtractivoDetailViews(generic.DetailView):
    model = Parada
    template_name = 'atractivo_detail.html'
    
def Parada(request):
    paradas = Parada.objects.all()
    return render(request, 'index.html',{'paradas': paradas})


def paradas_por_recorrido(request):
    #ANALIZAR ESTO PARA QUE NO SE PUEDAN REPETIR LOS NUMEROS DE PARADA EN EL ORDEN
    if request.method == 'POST':
        nombre_recorrido = request.POST.get('nombre_recorrido')
        paradas_del_recorrido = ParadaxRecorrido.objects.filter(recorrido__nombre=nombre_recorrido).order_by('nroParada')
        return render(request, 'paradas_por_recorrido.html', {'paradas_del_recorrido': paradas_del_recorrido})
    else:
        return render(request, 'index.html')
    

