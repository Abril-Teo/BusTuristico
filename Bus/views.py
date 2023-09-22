from django.views import generic
from django.shortcuts import render

from .models import Parada, Recorrido

# Create your views here.

def index(request):
    paradas = Parada.objects.all()
    return render(request, 'index.html',{'paradas': paradas})

class RecorridosListView(generic.ListView):
    model = Recorrido
    context_object_name = 'recorrido_list'   # your own name for the list as a template variable
    queryset = Recorrido.objects.all() # Get 5 books containing the title war
    template_name = 'recorridos.html'
    

class ParadasDetailViews(generic.DetailView):
    model = Parada
    template_name = 'parada_detail.html'