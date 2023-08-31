# BusTuristico


<details>
<summary>Diagrama de Clases UML</summary>

```mermaid
classDiagram


Viaje --> "1" Recorrido
Viaje --> "1" Bus
Viaje --> "1" Chofer

Bus --> "1..*" Cambio_Estado
Cambio_Estado --> "2" Estado

Recorrido --> "1..*" Parada
Parada --> "1..*" Atractivo

    class Recorrido{
        -String color
        -int duracion_aproximada
        -datetime hora_inicio_estimada
        -datetime hora_finalizacion_estimada
        -int frecuencia
        +definirOrdenParadas()
    }
    

    note for Recorrido "Ver como hacer con el orden de las paradas"

    class Parada{
        -String nombre
        -String direccion
        -String descripcion
        -String foto
        -ArrayList<Atractivo> atractivosCercanos 
        +conocerAtracciones()
    }
 

    class Atractivo{
        -String nombre
        -int calificacion
    }

    class Bus{
        -String patente
        -int num_unidad
        -datetime fecha_compra
        -Estado estado
        +conocer_estado()
    }

    class Cambio_Estado{
        -datetime fecha_cambio
        -Estado estado_anterior
        -Estado estado_nuevo
    }

    class Estado{
        -String Nombre
        -String descripcion
    }

    class Chofer{
        -String nombre
        -String apellido
        -String legajo
        +setNombre()
        +getNombre()
        +setLegajo()
        +getLegajo()
        +new()
    }

    note for Chofer "Los metodos set y get que se definen en la clase Chofer son extensivos a todas las clases del modelo"


    class Viaje{
        -Bus bus
        -Recorrido recorrido
        -Chofer chofer
        -time inicio_real
        -time final_real
        +duracion()
        +generar_ticket()
        +generar_reporte()
        +calcular_demora()
        +conocer_bus()
        +conocer_recorrido()
        +conocer_chofer()
        +definir_dupla()
        +buses_disponibles()
    }




```
</details>

