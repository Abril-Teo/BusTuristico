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
        -int duracion_aproximada
        -int hora_inicio
        -int hora_finalizacion
    }

    note for Recorrido "Ver como hacer con el orden de las paradas"

    class Parada{
        -String nombre
        -String direccion
        -String descripcion
        -String foto
    }

    class Atractivo{
        -String nombre
        -int calificacion
    }

    class Bus{
        -String patente
        -int num_patente
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
        -time inicio
        -time final
        +duracion()
        +generar_reporte()
        +calcular_demora()
        +conocer_bus()
        +conocer_recorrido()
        +conocer_chofer()
    }




```
</details>

