from django.urls import path, include
from django.contrib.auth.decorators import login_required, user_passes_test

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
    path('super/', user_passes_test(lambda u: u.is_superuser)(views.viewViaje), name='solosuper'),
    path('staff/', user_passes_test(lambda u: u.is_staff)(views.staffonly), name='staffonly'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('staff/<int:pk>', views.CargarViajeDetailViews.as_view(), name='cargar_viaje'),
    path('cargarchoffer/', views.newCofer, name='nuevoChofer'),
    path('ActualizarInicio/', views.ActualizarInicio, name='actualizarinicio'),
    path('ActualizarFinal/', views.ActualizarFinal, name='actualizarfinal'),
    path('emitirTicket/', views.EmitirTicket.as_view(), name='EmitirTicket'),
    path('generarReportes/', views.GenerarReportes, name='generarReporte'),
]

