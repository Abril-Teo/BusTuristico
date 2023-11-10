from django.urls import path, include
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views


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
    path('super/', user_passes_test(lambda u: u.is_superuser)(views.mostrarFormViaje), name='solosuper'),
    #path('crud/', user_passes_test(lambda u: u.is_superuser)(views.CrearViajeView.as_view()), name='lista_viajes'),
    path('super-recorrido-viaje/', user_passes_test(lambda u: u.is_superuser)(views.MostrarRecorridos), name='elegirRecorrido'),
    path('staff/', user_passes_test(lambda u: u.is_staff)(views.staffonly), name='staffonly'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('staff/<int:pk>', views.CargarViajeDetailViews.as_view(), name='cargar_viaje'),
    path('cargarchoffer/', views.newChofer, name='nuevoChofer'),
    path('cargarbus/', views.newBus, name='nuevoBus'),
    path('cargarrecorrido/', views.newRecorrido, name='nuevoRecorrido'),
    path('cargarparada/', views.newParada, name='nuevaParada'),
    path('cargarparadaxrecorrido/', views.newParadaXRecorrido, name='nuevaParadaXRecorrido'),
    path('ActualizarInicio/', views.ActualizarInicio, name='actualizarinicio'),
    path('ActualizarFinal/', views.ActualizarFinal, name='actualizarfinal'),
    path('emitirTicket/', views.EmitirTicket, name='EmitirTicket'),
    path('generarReportes/', views.GenerarReportes, name='generarReporte'),
    path('cambiar-contrasena/', auth_views.PasswordChangeView.as_view(), name='cambiar_contraseña'),
    path('cambiar_estado_bus/', views.cambiar_estado_bus, name = 'cambiar_estado_bus'),
    path('super/crearViaje/', views.newViaje, name = 'crear_viaje'),
    path('crud/listar', views.listar_viajes, name='listar_viajes'),
    path('crud/editar/<int:pk>/', views.editar_viaje, name='editar_viaje'),
    path('crud/eliminar/<int:pk>/', views.eliminar_viaje, name='eliminar_viaje'),
    
]

