from django.contrib import admin
from .models import Atractivo, Bus, Chofer, Estado,CambioEstado, Parada, ParadaxRecorrido, Recorrido, Viaje

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    search_fields = ('patente','numUnidad')
    list_display = ('patente','numUnidad','fechaCompra')
    list_filter = ('patente',)

admin.site.register(Bus,BusAdmin)
admin.site.register(Chofer)
admin.site.register(Viaje)
admin.site.register(Estado)
admin.site.register(ParadaxRecorrido)
admin.site.register(Parada)
admin.site.register(Atractivo)
admin.site.register(CambioEstado)
admin.site.register(Recorrido)