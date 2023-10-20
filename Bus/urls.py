from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Recorridos/RecorridoDetalle/<int:pk>', views.ParadasDetailViews.as_view(), name='parada-detail'),
    path('Recorridos/atractivos/<int:pk>', views.AtractivoDetailViews.as_view(), name='atractivo-detail'),
    path("Recorridos/", views.RecorridosListView.as_view(), name="recorridos"),
    path("Recorridos/RecorridoDetalle/", views.paradas_por_recorrido, name="paradas_por_recorrido"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('chofferes/', views.cargaRecorridos, name='cargaRecorridos'),
    path('accounts/vista_login/', views.vista_login, name='vista_login'),
    path('accounts/vista_login/comprobacion', views.logincomprobacion, name='login_comprobacion'),
    path('super/', views.superuseronly, name='superonly'),
    path('staff/', views.staffonly, name='staffonly'),
]

