from datetime import date, timedelta
from datetime import datetime
import json


from django.shortcuts import get_object_or_404, render, redirect
from .models import Bus, CambioEstado, Estado 

#from io import BytesIO
#from tkinter import Canvas
from django.views import View, generic
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize

from Bus.templatetags import jinja2_custom_filters
from .forms import *
from .models import Chofer, Viaje, Bus, Recorrido, Parada
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import jinja2
import pdfkit





from .models import Atractivo, Parada, Recorrido, ParadaxRecorrido
from django.shortcuts import render

def vista_login(request):
    return render(request, 'login.html')


def logincomprobacion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('index')
            if user.is_staff:
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})


def index(request):
    return render(request, 'index.html')

def hopOnHopOff(request):
    return render(request, 'hopOnHopOff.html')

class RecorridosListView(generic.ListView):
    model = Recorrido
    context_object_name = 'recorrido_list' 
    queryset = Recorrido.objects.all() 
    template_name = 'recorridos.html'
        

class ParadasDetailViews(generic.DetailView):
    model = Parada
    template_name = 'parada_detail.html'
    
class AtractivoDetailViews(generic.DetailView):
    model = Atractivo
    template_name = 'atractivo_detail.html'

class CargarViajeDetailViews(UpdateView, DetailView):
    model = Viaje
    template_name = 'cambiarHora_viaje.html'
    fields = ['inicio_real', 'final_real']
    


def paradas_por_recorrido(request):
    if request.method == 'POST':
        id_recorrido = request.POST.get('nombre_recorrido')
        recorrido = Recorrido.objects.get(id=id_recorrido)
        paradas_del_recorrido = ParadaxRecorrido.objects.filter(recorrido__id=id_recorrido).order_by('nroParada')
        return render(request, 'paradas_por_recorrido.html', {'paradas_del_recorrido': paradas_del_recorrido, 'recorrido': recorrido})
    else:
        return render(request, 'index.html')
    
def cerrar_sesion(request):
    logout(request)
    return redirect('index') 
@login_required
def cargaRecorridos(request):
    return render(request, 'cargaRecorridos.html')

@user_passes_test(lambda u: u.is_superuser)
def superuseronly(request):
    return render(request, 'solosuper.html')

@user_passes_test(lambda u: u.is_staff)
def staffonly(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            print("super")
            viajesHoy = Viaje.objects.filter(fecha=date.today()).order_by('inicio_estimado')
            return render(request, 'solostaff.html', {'viajes_choffer': viajesHoy})
        if request.user.is_staff:
            print("staff")
            dni_chofer = request.user.username
            viajes_del_chofer = Viaje.objects.filter(chofer__dni=dni_chofer).filter(fecha=date.today()).order_by('inicio_estimado')
            return render(request, 'solostaff.html', {'viajes_choffer': viajes_del_chofer})
    else:
        return render(request, 'index.html')

def mostrarFormViaje(request):
    formulario = NuevoViaje()
    return render(request, 'solosuper.html', {'formulario': formulario})
def newViaje(request):
    if request.method == 'POST':
        idViaje = request.POST.get('idViaje')
        recorrido_seleccionado = request.POST.get('recorrido_seleccionado')
        viaje = Viaje.objects.get(nro_viaje=idViaje)
        recorrido = Recorrido.objects.get(id=recorrido_seleccionado)
        viaje.recorrido = recorrido
        viaje.save()
    return redirect(index)

def MostrarRecorridos(request):
    formulario = NuevoViaje(request.POST)
    if formulario.is_valid():
        nuevo_objeto = Viaje(
            nro_viaje=formulario.cleaned_data['nroViaje'] ,
            fecha=formulario.cleaned_data['fecha'], 
            inicio_real= None,
            final_real= None,
            inicio_estimado=formulario.cleaned_data['inicioEstimado'], 
            final_estimado=formulario.cleaned_data['finalEstimado'], 
            chofer=None, 
            bus=None, 
            recorrido=None,
        )
        nuevo_objeto.save()

    inicio = request.POST.get('inicioEstimado')
    final = request.POST.get('finalEstimado')
    print(inicio,final)
    final = datetime.datetime.strptime(final, "%H:%M").time()
    inicio = datetime.datetime.strptime(inicio, "%H:%M").time()

# Realiza la resta
    duracion_seleccionada = timedelta(hours=final.hour, minutes=final.minute) - timedelta(hours=inicio.hour, minutes=inicio.minute)
    duracion_en_minutos = duracion_seleccionada.total_seconds() / 60
    print(duracion_en_minutos)
    if duracion_seleccionada:
        recorridos_filtrados = Recorrido.objects.filter(duracionAprox=duracion_en_minutos)
        serialized_recorridos = serialize('json', recorridos_filtrados)
        return JsonResponse({'recorridos': serialized_recorridos})
    else:
        return JsonResponse({'error': 'Algo salió mal'})
    
    
    
def listar_viajes(request):
    viajes = Viaje.objects.all()
    return render(request, 'listar_viajes.html', {'viajes': viajes})

def editar_viaje(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)

    if request.method == 'POST':
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            return redirect('listar_viajes')
    else:
        form = ViajeForm(instance=viaje)

    return render(request, 'editar_viaje.html', {'form': form, 'viaje': viaje})
def eliminar_viaje(request, pk):
    viaje = get_object_or_404(Viaje, pk=pk)
    viaje.delete()
    return redirect('listar_viajes')

def newChofer(request):
    if request.method == 'POST':
        formulario = NuevoChofer(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Chofer(nombre=datos_formulario['nombre'] ,apellido=datos_formulario['apellido'], legajo=datos_formulario['legajo'], dni=datos_formulario['dni'])
            nuevo_objeto.save()
            username = datos_formulario['dni']
            password = datos_formulario['legajo']
            name = datos_formulario['nombre']
            lastname = datos_formulario['apellido']
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.first_name = name
            user.last_name = lastname
            user.is_staff = True
            user.save()
            
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})


def newBus(request):
    if request.method == 'POST':
        formulario = NuevoBus(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Bus(patente=datos_formulario['patente'] ,numUnidad=datos_formulario['numUnidad'], fechaCompra=datos_formulario['fechaCompra'], estado=datos_formulario['estado'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})


def newRecorrido(request):
    if request.method == 'POST':
        formulario = NuevoRecorrido(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Recorrido(nombre=datos_formulario['nombre'] ,hex_color=datos_formulario['color'], duracionAprox=datos_formulario['duracionAprox'],
                                      horaInicioAprox=datos_formulario['horaInicioAprox'], horaFinalizacionAprox=datos_formulario['horaFinalizacionAprox'], frecuencia=datos_formulario['frecuencia'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid WTF")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})


def newParada(request):
    if request.method == 'POST':
        formulario = NuevaParada(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Parada(nombre=datos_formulario['nombre'] ,calle=datos_formulario['calle'], numero=datos_formulario['numero'],
                                      descripcion=datos_formulario['descripcion'], foto=datos_formulario['foto'], atractivos=datos_formulario['atractivos'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})


def newParadaXRecorrido(request):
    if request.method == 'POST':
        formulario = AgregarParada(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = ParadaxRecorrido(nroParada=datos_formulario['nroParada'] ,llegadaEstimada=datos_formulario['llegadaEstimada'], recorrido=datos_formulario['recorrido'], parada=datos_formulario['parada'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    return render(request, 'solosuper.html', {'formulario': formulario})


def ActualizarInicio(request):
    if request.method == 'POST':
        viaje_id = request.POST.get('id')
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.inicio_real = datetime.datetime.now()
        viaje.save()
        return redirect(f'/bus/staff/{viaje_id}')

    return HttpResponse(status=200)
def ActualizarFinal(request):
    if request.method == 'POST':
        viaje_id = request.POST.get('id')
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.final_real = datetime.datetime.now()
        viaje.save()
        return redirect(f'/bus/staff/{viaje_id}')

    """aca se generara un pdf con los datos pedidos(número de viaje
            asignado, la fecha y hora de inicio y fin real del viaje, el número de unidad, el legajo y
            nombre completo del chofer, la duración en minutos y el recorrido realizado.)"""
def EmitirTicket(request):
    if request.method == 'POST':
        id_viaje = request.POST.get('id')
        viaje = Viaje.objects.get(id=id_viaje)
        try:
            env = jinja2.Environment(loader = jinja2.FileSystemLoader('Bus/templates'))
            template = env.get_template('ticketTemplate.html')
            fecha = viaje.fecha
            dia = fecha.strftime("%d-%m-%Y")
            nombrecompleto = f'{viaje.chofer.nombre} {viaje.chofer.apellido}' 
            fecha_inicial_real = datetime.datetime(2023, 10, 17, viaje.inicio_real.hour, viaje.inicio_real.minute, viaje.inicio_real.second)
            fecha_final_real = datetime.datetime(2023, 10, 17, viaje.final_real.hour, viaje.final_real.minute, viaje.final_real.second)
            duracion = fecha_final_real - fecha_inicial_real
            duracion_en_minutos = round(duracion.total_seconds() / 60)
            hoy = datetime.datetime.now()
            
            html = template.render({"nroViaje": viaje.nro_viaje, "fecha": dia, "inicio": viaje.inicio_real, "final": viaje.final_real, "nro_unidad": viaje.bus.numUnidad, "legajo": viaje.chofer.legajo, "nombre": nombrecompleto, "recorrido": viaje.recorrido.nombre, "duracion": duracion_en_minutos, "fechaHoy": hoy})
            
            options = {
                'page-size': 'Letter',
                'encoding': "UTF-8",
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in'
            }
            
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            pdf = pdfkit.from_string(html, False, configuration=config, options=options)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Ticket.pdf"'

            return response
        except Exception as e:
            print(e)
            return HttpResponse("le faltan datos al viaje ejemplo")
        

def GenerarReportes(request):
    viajes = Viaje.objects.filter(fecha=date.today()).order_by('inicio_real')
    if len(viajes) != 0:
        diferencias = []
        acumuladorduracion = 0
        promedio_diferencias = timedelta(0)
        promedio_duracion = 0
        viajesValidos = []

        for viaje in viajes:
            if viaje.inicio_real is not None and viaje.final_real is not None:
                viajesValidos.append(viaje)
                fecha_inicial_real = datetime.datetime(2023, 10, 17, viaje.inicio_real.hour, viaje.inicio_real.minute, viaje.inicio_real.second)
                fecha_final_real = datetime.datetime(2023, 10, 17, viaje.final_real.hour, viaje.final_real.minute, viaje.final_real.second)
                fecha_inicial_estimado = datetime.datetime(2023, 10, 17, viaje.inicio_estimado.hour, viaje.inicio_estimado.minute, viaje.inicio_estimado.second)
                duracion = fecha_final_real - fecha_inicial_real
                duracion_en_minutos = round(duracion.total_seconds() / 60)
                acumuladorduracion += duracion_en_minutos
                if fecha_inicial_estimado > fecha_inicial_real:
                    demorainicio = fecha_inicial_estimado - fecha_inicial_real
                    diferencias.append(demorainicio.total_seconds())  
                else:
                    demorainicio = fecha_inicial_real - fecha_inicial_estimado
                    diferencias.append(-demorainicio.total_seconds())  

        suma_diferencias = timedelta(0)

        for diferencia_segundos in diferencias:
            diferencia_timedelta = timedelta(seconds=diferencia_segundos)
            suma_diferencias += diferencia_timedelta
            

        cantidad_viajes = len(diferencias)
        if cantidad_viajes > 0:
            promedio_diferencias = suma_diferencias / cantidad_viajes
            promedio_duracion = int(acumuladorduracion / cantidad_viajes)

        promedio_en_minutos = round(promedio_diferencias.total_seconds() / 60)
        promedio_horas = promedio_en_minutos // 60
        promedio_minutos = promedio_en_minutos % 60

        if promedio_en_minutos > 0:
            promedioinicio = f"{promedio_horas} horas y {promedio_minutos} minutos adelantado"
        elif promedio_en_minutos < 0:
            promedioinicio = f"{-promedio_horas} horas y {promedio_minutos} minutos demorado"
        else:
            promedioinicio = "En hora"
            
        if viajesValidos != []:
            env = jinja2.Environment(loader = jinja2.FileSystemLoader('Bus/templates'))
            jinja2_custom_filters.register_custom_filters(env) 
            template = env.get_template('pdftemplate.html')
            fecha = datetime.datetime.now()
            dia = fecha.date().strftime("%d-%m-%Y")
            html = template.render({"dia":dia,"viajes":viajesValidos, "promedioinicio":promedioinicio, "promedioduracion": promedio_duracion})
            
            options = {
                'page-size': 'Letter',
                'encoding': "UTF-8",
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in'
            }
            
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            pdf = pdfkit.from_string(html, False, configuration=config, options=options)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Reporte_diario.pdf"'

            return response
        return HttpResponse("No hay viajes en el dia")
    else:
        return HttpResponse("No hay viajes en el dia")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def cambiar_estado_bus(request, bus_id):
    if request.method == 'POST':
        bus = Bus.objects.get(pk=bus_id)
        nuevo_estado_habilitado = not bus.isHabilitado()
        
        # Crear un nuevo registro de cambio de estado
        cambio_estado = CambioEstado(estadoAnterior=bus.estado, estadoNuevo=nuevo_estado_habilitado, motivo="Cambio de estado por administrador")
        cambio_estado.save()
        # Actualizar el estado del autobús
        bus.estado = cambio_estado
        return redirect('cambiar_estado_bus')  # Reemplaza 'pagina_deseada' con el nombre de tu vista

    bus = Bus.objects.get(pk=bus_id)
    return render(request, 'cambiar_estado_bus.html')


