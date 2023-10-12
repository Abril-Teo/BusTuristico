from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Recorridos/RecorridoDetalle/<int:pk>', views.ParadasDetailViews.as_view(), name='parada-detail'),
    path('Recorridos/RecorridoDetalle/<int:pk>/<int:pk>', views.AtractivoDetailViews.as_view(), name='parada-detail'),
    path("Recorridos/", views.RecorridosListView.as_view(), name="recorridos"),#se mostraran los recorridos
    path("Recorridos/RecorridoDetalle/", views.paradas_por_recorrido, name="paradas_por_recorrido"),
]

