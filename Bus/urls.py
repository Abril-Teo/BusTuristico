from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recorridos/<int:pk>', views.ParadasDetailViews.as_view(), name='parada-detail'),
    path("recorridos/", views.RecorridosListView.as_view(), name="recorridos"),
    
]

