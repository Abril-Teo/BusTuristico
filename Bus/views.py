from datetime import date, timedelta
from datetime import datetime
from io import BytesIO
from tkinter import Canvas
from django.views import View, generic
from django.views.generic import DetailView, UpdateView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from Bus.templatetags import jinja2_custom_filters
from .forms import NuevoChofer, NuevoViaje
from .models import Chofer, Viaje
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import jinja2
import pdfkit


#FALTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA LO DE DEFINIR DUPLA Y LO DE CAMBIAR ESTADO Y QUE SOLO SE MUESTREN LOS COLECTIVOS QUE ESTAN HABILITADOS PARA ANDAR

from .models import Atractivo, Parada, Recorrido, ParadaxRecorrido

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
                return redirect('solosuper')
            if user.is_staff:
                login(request, user)
                return HttpResponseRedirect('/bus/staff/')

            #  ....
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
        nombre_recorrido = request.POST.get('nombre_recorrido')
        paradas_del_recorrido = ParadaxRecorrido.objects.filter(recorrido__nombre=nombre_recorrido).order_by('nroParada')
        return render(request, 'paradas_por_recorrido.html', {'paradas_del_recorrido': paradas_del_recorrido})
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
        dni_chofer = request.user.username
        viajes_del_chofer = Viaje.objects.filter(chofer__dni=dni_chofer).filter(fecha=date.today()).order_by('inicio_estimado')
        return render(request, 'solostaff.html', {'viajes_choffer': viajes_del_chofer})
    else:
        return render(request, 'index.html')
    #return render(request, 'solostaff.html')


def viewViaje(request):
    if request.method == 'POST':
        formulario = NuevoViaje(request.POST)
        if formulario.is_valid():
            datos_formulario = formulario.cleaned_data
            nuevo_objeto = Viaje(nro_viaje=datos_formulario['nroViaje'] ,fecha=datos_formulario['fecha'], inicio_estimado=datos_formulario['inicioEstimado'], final_estimado=datos_formulario['finalEstimado'], chofer=datos_formulario['chofer'], bus=datos_formulario['bus'],recorrido=datos_formulario['recorrido'])
            nuevo_objeto.save()
            return redirect('solosuper')
        else:    
            print("not valid")
    else:
        formulario = NuevoViaje()
    
    return render(request, 'solosuper.html', {'formulario': formulario})

def newCofer(request):
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

def ActualizarInicio(request):
    if request.method == 'POST':
        viaje_id = request.POST.get('id')
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.inicio_real = datetime.now()
        viaje.save()
        return redirect(f'/bus/staff/{viaje_id}')

    return HttpResponse(status=200)
def ActualizarFinal(request):
    if request.method == 'POST':
        viaje_id = request.POST.get('id')
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.final_real = datetime.now()
        viaje.save()
        return redirect(f'/bus/staff/{viaje_id}')

    """aca se generara un pdf con los datos pedidos(número de viaje
            asignado, la fecha y hora de inicio y fin real del viaje, el número de unidad, el legajo y
            nombre completo del chofer, la duración en minutos y el recorrido realizado.)"""
class EmitirTicket(View):
    def get(self, request, *args, **kwargs):
        # Datos que deseas incluir en el PDF
        datos = {
            'nombre': 'John Doe',
            'edad': 30,
            'ocupacion': 'Desarrollador'
        }

        # Crea un objeto "response" para el PDF
        response = FileResponse(self.crear_pdf(datos))
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="archivo.pdf"'
        return response

    def crear_pdf(self, datos):
        response = BytesIO()
        pdf = Canvas(response)

        # Agrega contenido al PDF
        pdf.drawString(100, 750, "Información del usuario:")
        pdf.drawString(100, 730, f"Nombre: {datos['nombre']}")
        pdf.drawString(100, 710, f"Edad: {datos['edad']}")
        pdf.drawString(100, 690, f"Ocupación: {datos['ocupacion']}")

        # Cierra el objeto Canvas
        pdf.showPage()
        pdf.save()
        response.seek(0)

        return response
#incluye la duración en minutos, la demora de inicio del viaje respecto a la hora programada,
#y el promedio diario de ambos valores QUEDAAAAAAAAAAAAAAAAAAAAAAAAAAA PASARLO A PDF
def GenerarReportes(request):
    viajes = Viaje.objects.filter(fecha=date.today()).order_by('inicio_real')
    diferencias = []

    for viaje in viajes:
        fecha_inicial_real = datetime(2023, 10, 17, viaje.inicio_real.hour, viaje.inicio_real.minute, viaje.inicio_real.second)
        fecha_final_real = datetime(2023, 10, 17, viaje.final_real.hour, viaje.final_real.minute, viaje.final_real.second)
        fecha_inicial_estimado = datetime(2023, 10, 17, viaje.inicio_estimado.hour, viaje.inicio_estimado.minute, viaje.inicio_estimado.second)
        duracion = fecha_final_real - fecha_inicial_real
        if fecha_inicial_estimado > fecha_inicial_real:
            demorainicio = fecha_inicial_estimado - fecha_inicial_real
            diferencias.append(demorainicio.total_seconds())  
        else:
            demorainicio = fecha_inicial_real - fecha_inicial_estimado
            diferencias.append(-demorainicio.total_seconds())  

    promedio_diferencias = timedelta(0)

    for diferencia_segundos in diferencias:
        diferencia_timedelta = timedelta(seconds=diferencia_segundos)
        promedio_diferencias += diferencia_timedelta

    cantidad_viajes = len(diferencias)
    if cantidad_viajes > 0:
        promedio_diferencias = promedio_diferencias / cantidad_viajes

    promedio_en_minutos = round(promedio_diferencias.total_seconds() / 60)
    promedio_horas = promedio_en_minutos // 60
    promedio_minutos = promedio_en_minutos % 60

    if promedio_en_minutos > 0:
        promedioinicio = f"{promedio_horas} horas y {promedio_minutos} minutos adelantado"
    elif promedio_en_minutos < 0:
        promedioinicio = f"{promedio_horas} horas y {promedio_minutos} minutos demorado"
    else:
        promedioinicio = "En hora"

    print("promedio en minutos:", promedio_en_minutos)
    print("Promedio Inicio:", promedioinicio)
        

    env = jinja2.Environment(loader = jinja2.FileSystemLoader('Bus/templates'))
    jinja2_custom_filters.register_custom_filters(env) 
    template = env.get_template('pdftemplate.html')
    fecha = datetime.now()
    dia = fecha.date().strftime("%d-%m-%Y")
    html = template.render({"dia":dia,"viajes":viajes, "duracion":duracion, "promedioinicio":promedioinicio})
    
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

        