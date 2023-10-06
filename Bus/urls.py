from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Recorridos/<int:pk>', views.ParadasDetailViews.as_view(), name='parada-detail'),
    path("recorridos/", views.RecorridosListView.as_view(), name="recorridos"),#se mostraran los recorridos
    path("Recorridos/", views.paradas_por_recorrido, name="paradas_por_recorrido"),
]

