from django.contrib import admin
from .models import Atractivo, Bus, Chofer, Estado,CambioEstado, Parada, ParadaxRecorrido, Recorrido, Viaje
from django.contrib.auth.models import User

class BusAdmin(admin.ModelAdmin):
    search_fields = ('patente','numUnidad')
    list_display = ('patente','numUnidad','fechaCompra')
    list_filter = ('patente',)
    
    

class ChoferAdmin(admin.ModelAdmin):
    list_display = ['dni', 'legajo','nombre','apellido']
    def save_model(self, request, obj, form, change):
        username = obj.dni
        password = obj.legajo
        name = obj.nombre
        lastname = obj.apellido
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.first_name = name
        user.last_name = lastname
        user.is_staff = True
        user.save()
        obj.save()

admin.site.register(Chofer, ChoferAdmin)

admin.site.register(Bus,BusAdmin)
admin.site.register(Viaje)
admin.site.register(Estado)
admin.site.register(ParadaxRecorrido)
admin.site.register(Parada)
admin.site.register(Atractivo)
admin.site.register(CambioEstado)
admin.site.register(Recorrido)