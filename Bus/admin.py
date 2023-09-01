from django.contrib import admin
from .models import Bus, Estado,CambioEstado

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    search_fields = ('patente','numUnidad')
    list_display = ('patente','numUnidad','fechaCompra')
    list_filter = ('patente',)

admin.site.register(Bus,BusAdmin)
admin.site.register(Estado)