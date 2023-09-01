from django.shortcuts import render

from .models import Bus

# Create your views here.

def index(request):
    buses = Bus.objects.all()
    return render(request, 'index.html',{'bus': buses})