# BusTuristico
Es un proyecto django creado por integrantes de un grupo del instituto tecnico salesiano villada para un bus turistico de Buenos Aires, que tiene las siguientes funcionalidades:
- visualizacion de recorridos, atractivos y paradas del lado del usuario
- creacion de viajes, reportes diarios del lado del administrador, ademas de poder llevar un registro de los colectivos habilitados y los choferes que esta activos
- carga de tiempo de viajes de los chofferes y generacion de tickets

<details>
<summary>Diagrama de Clases UML</summary>

```mermaid
classDiagram
    Viaje --> "1" Bus
    Viaje --> "1" Chofer
    
    Bus --> "1..*" CambioEstado
    Viaje --> "1" Recorrido
    Recorrido --> "1" ParadaxRecorrido
    ParadaxRecorrido --> "1..*" Parada
    Parada --> "1..*" Atractivo
    CambioEstado --> "1" Estado

    class Recorrido{
        -String color
        -int duracion_aproximada
        -datetime hora_inicio_estimada
        -datetime hora_finalizacion_estimada
        -int frecuencia
        +new()
    }
    class Parada{
        -String nombre
        -String descripcion
        -String calle
        -Int numero
        -String foto
        -Atractivo listaAtractivos
        +mostrarAtractivosCercanos()
        +conocerAtractivosCercanos()
        +definirOrdenParadas()
        +new()
    }
    class Atractivo{
        -String nombre
        -String calle
        -Int numero
        -String descripcion
        -String foto
        -Int calificacion
        -Int distancia_parada
        +new()
    }
    class Bus{
        -String patente
        -Int num_unidad
        -Datetime fecha_compra
        -CambioEstado estado
        +conocer_estado()
        +isHabilitado()
        +new()

    }
    class CambioEstado{
        -Datetime fecha_cambio
        -String motivo
        -Estado estado_nuevo
        -Estado estado_anterior
        +new()
    }
    class Estado{
        -String nombre
        -Boolean habilitado
        -String detalles
        +new()
    }
    class Chofer{
        -String nombre
        -String apellido
        -String legajo
        -Int dni
        +Setnombre()
        +getnombre()
        +Setapellido()
        +getapellido()
        +Setlegajo()
        +getlegajo()
        +Setdni()
        +getdni()
        +new()
    }
    note for Chofer "Los setters y getters se extienden a todo el diagrama con los atributos respectivos a cada clase"

    class Viaje {
        -Int numero_viaje
        -String color
        -Bus bus
        -Chofer chofer
        -Date fecha
        -Datetime inicio_real
        -Datetime final_real
        -Datetime inicio_estimado
        -Datetime final_estimado
        +calcularPromedioInicio-Duracion()
        +calcularFinalEstimado()
        +newViaje()
        +conocerRecorrido()
        +ingresarInicio()
        +ingresarFin()
        +calcularDuracionEstimada()
        +calcularDuracionFinal()
        +generarInformeViaje()
        +conocerBus()
        +conocerChofer()
    }

    class ParadaxRecorrido {
        -Recorrido recorrido
        -Parada parada
        -int nroParada
        -time llegadaEstimada
        +new()
        +DefinirOrdenParadas()
    }
```
</details>


<details>
<summary>Diagrama entidad relacion.</summary>

```erDiagram
Recorrido{
        String color
        int duracion_aproximada
        datetime hora_inicio_estimada
        datetime hora_finalizacion_estimada
        int frecuencia
    }

    Parada{
        String nombre
        String descripcion
        String calle
        Int numero
        String foto
        Atractivo listaAtractivos
    }

    Atractivo{
        String nombre
        String calle
        Int numero
        String descripcion
        String foto
    }

    Bus{
        String patente
        Int num_unidad
        Datetime fecha_compra
        CambioEstado estado
    }

    CambioEstado{
        Datetime fecha_cambio
        String motivo
    }

    Estado{
        String nombre
        Boolean habilitado
        String detalles    
    }

    Chofer{
        String nombre
        String apellido
        String legajo
        Int dni
    }

    Viaje {
        Int numero_viaje
        String color
        Bus bus
        Chofer chofer
        Date fecha
        Datetime inicio_real
        Datetime final_real
        Datetime inicio_estimado
        Datetime final_estimado
    }

    ParadaxRecorrido {
        Recorrido recorrido
        Parada parada
        int nroParada
        datetime llegadaEstimada
    }
```
</details>
