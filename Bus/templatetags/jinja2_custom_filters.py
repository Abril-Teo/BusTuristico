# jinja2_custom_filters.py
from datetime import datetime
from jinja2 import Environment

def calcular_demora_inicio(fecha_inicial_real, fecha_inicial_estimado):
    fecha_inicial_estimado = datetime(2023, 10, 17, fecha_inicial_estimado.hour, fecha_inicial_estimado.minute, fecha_inicial_estimado.second)
    fecha_inicial_real = datetime(2023, 10, 17, fecha_inicial_real.hour, fecha_inicial_real.minute, fecha_inicial_real.second)
    
    if fecha_inicial_estimado > fecha_inicial_real:
        demorainicio = fecha_inicial_estimado - fecha_inicial_real
        return str(demorainicio) + " adelantado"
    else:
        demorainicio = fecha_inicial_real - fecha_inicial_estimado
        return str(demorainicio) + " demorado"

def calcular_duracion(inicio, final):
    inicio = datetime(2023, 10, 17, inicio.hour, inicio.minute, inicio.second)
    final = datetime(2023, 10, 17, final.hour, final.minute, final.second)
    duracion = final - inicio
    return round(duracion.total_seconds() / 60)
    
# Registra la función en el entorno de Jinja2
def register_custom_filters(env):
    env.filters['calcular_demora_inicio'] = calcular_demora_inicio
    env.filters['calcular_duracion'] = calcular_duracion
env = Environment()
register_custom_filters(env)
