from django.contrib import admin
from .models import Atractivo, Bus, Chofer, Estado,CambioEstado, Parada, ParadaxRecorrido, Recorrido, Viaje
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    search_fields = ('patente','numUnidad')
    list_display = ('patente','numUnidad','fechaCompra')
    list_filter = ('patente',)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename','name')
    
    

class ChoferAdmin(admin.ModelAdmin):
    list_display = ['dni', 'legajo']
    def save_model(self, request, obj, form, change):
        username = obj.dni
        password = obj.legajo
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
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
admin.site.register(Permission,PermissionAdmin)