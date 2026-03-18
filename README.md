Proyecto-Final-1400
Widget Flotante Pomodoro

Desarrollo del Diseño

Proyecto: Widget Flotante Pomodoro
El programa consiste en un widget flotante que ayuda al usuario a organizar sus tareas usando la técnica Pomodoro. El sistema permite:

agregar tareas,
asignar prioridades,
seleccionar una tarea,
ingresar un tiempo de enfoque,
iniciar un temporizador,
pausar, reiniciar, completar o eliminar tareas,
y repetir sesiones de trabajo.

El diseño lógico del programa incluye:

Condicional 1: verificar si el usuario desea agregar una tarea.
Condicional 2: verificar si la prioridad fue seleccionada correctamente.
Condicional 3: verificar si el tiempo ingresado es válido.
ondicional 4: verificar si el tiempo terminó.
Bucle: mientras el tiempo restante sea mayor que cero, el temporizador sigue contando hacia atrás

Explicación del Flowchart

El flujo del programa comienza con la inicialización del sistema y la creación de variables principales, como la lista de tareas y el temporizador.

Después, el widget flotante se muestra en pantalla con los botones de acción. El sistema queda esperando una acción del usuario.

Rutas principales del flujo:

1. Agregar tarea

   El usuario escribe el nombre de la tarea.
   El sistema verifica si se seleccionó una prioridad.
   Si la prioridad es válida, se asigna un color:

     Alta = rojo
     Media = amarillo
     Baja = verde
     Luego la tarea se guarda y la interfaz se actualiza.

2. Iniciar temporizador

   El usuario selecciona una tarea.
   Ingresa el tiempo de enfoque.
   El sistema valida si el tiempo es correcto.
   Si es válido, inicia el temporizador.
   Mientras el tiempo restante sea mayor a 0, el sistema:

     -muestra el tiempo en pantalla,
     -espera un segundo,
     -reduce el contador.
    Al terminar, muestra un mensaje motivacional y marca la tarea como completada.

3. Nueva sesión

   El sistema pregunta si el usuario desea iniciar otra sesión.
   Si responde sí, vuelve al flujo principal.
   Si responde no, finaliza el programa.


Pseudocódigo

#Widget Flotante Pomodoro

```text
INICIO

# ----------------------------------------
# Inicialización del programa
# ----------------------------------------

Mostrar "Bienvenido al Widget Flotante Pomodoro"
Mostrar "Este programa te ayudará a organizar tareas y sesiones de enfoque"

Crear lista_tareas vacía
Crear tarea_seleccionada = vacío
Crear tiempo_restante = 0
Crear temporizador_activo = Falso
Crear opcion = ""

# ----------------------------------------
# Bucle principal del sistema
# ----------------------------------------

MIENTRAS opcion != "salir"

    Mostrar "-----------------------------------"
    Mostrar "Opciones disponibles:"
    Mostrar "1. Agregar tarea"
    Mostrar "2. Iniciar temporizador"
    Mostrar "3. Pausar temporizador"
    Mostrar "4. Reiniciar temporizador"
    Mostrar "5. Completar tarea"
    Mostrar "6. Eliminar tarea"
    Mostrar "7. Ver lista de tareas"
    Mostrar "8. Salir"

    Leer opcion

    # ----------------------------------------
    # Opción 1: Agregar tarea
    # ----------------------------------------
    SI opcion == "1" ENTONCES
        Mostrar "Ingrese el nombre de la tarea:"
        Leer nombre_tarea

        Mostrar "Seleccione prioridad: alta, media o baja"
        Leer prioridad

        SI prioridad == "alta" O prioridad == "media" O prioridad == "baja" ENTONCES
            
            SI prioridad == "alta" ENTONCES
                color = "rojo"
            SINO SI prioridad == "media" ENTONCES
                color = "amarillo"
            SINO
                color = "verde"
            FIN SI

            Guardar nombre_tarea y prioridad en lista_tareas
            Mostrar "Tarea agregada correctamente"
            Mostrar "Color asignado según prioridad: " + color

        SINO
            Mostrar "Error: prioridad no válida"
        FIN SI
    FIN SI

    # ----------------------------------------
    # Opción 2: Iniciar temporizador
    # ----------------------------------------
    SI opcion == "2" ENTONCES
        
        SI lista_tareas está vacía ENTONCES
            Mostrar "No hay tareas registradas"
        SINO
            Mostrar "Seleccione una tarea de la lista"
            Mostrar lista_tareas
            Leer tarea_seleccionada

            Mostrar "Ingrese el tiempo de enfoque en minutos:"
            Leer tiempo_ingresado

            SI tiempo_ingresado > 0 ENTONCES
                tiempo_restante = tiempo_ingresado * 60
                temporizador_activo = Verdadero

                Mostrar "Temporizador iniciado"

                MIENTRAS tiempo_restante > 0 Y temporizador_activo == Verdadero
                    Mostrar "Tiempo restante: " + tiempo_restante + " segundos"
                    Esperar 1 segundo
                    tiempo_restante = tiempo_restante - 1
                FIN MIENTRAS

                SI tiempo_restante == 0 ENTONCES
                    Mostrar "¡Tiempo terminado!"
                    Mostrar "Excelente trabajo, sigue así. Te has ganado un regalo sorpresa."
                    Mostrar "La tarea puede marcarse como completada"
                FIN SI

            SINO
                Mostrar "Error: el tiempo debe ser mayor que cero"
            FIN SI
        FIN SI
    FIN SI

    # ----------------------------------------
    # Opción 3: Pausar temporizador
    # ----------------------------------------
    SI opcion == "3" ENTONCES
        SI temporizador_activo == Verdadero ENTONCES
            temporizador_activo = Falso
            Mostrar "Temporizador pausado"
        SINO
            Mostrar "No hay temporizador en ejecución"
        FIN SI
    FIN SI

    # ----------------------------------------
    # Opción 4: Reiniciar temporizador
    # ----------------------------------------
    SI opcion == "4" ENTONCES
        tiempo_restante = 0
        temporizador_activo = Falso
        Mostrar "Temporizador reiniciado"
    FIN SI

    # ----------------------------------------
    # Opción 5: Completar tarea
    # ----------------------------------------
    SI opcion == "5" ENTONCES
        Mostrar "Seleccione la tarea que desea completar"
        Mostrar lista_tareas
        Leer tarea_seleccionada
        Marcar tarea_seleccionada como completada
        Mostrar "Tarea completada con éxito"
    FIN SI

    # ----------------------------------------
    # Opción 6: Eliminar tarea
    # ----------------------------------------
    SI opcion == "6" ENTONCES
        Mostrar "Seleccione la tarea que desea eliminar"
        Mostrar lista_tareas
        Leer tarea_seleccionada
        Eliminar tarea_seleccionada de lista_tareas
        Mostrar "Tarea eliminada correctamente"
    FIN SI

    # ----------------------------------------
    # Opción 7: Ver tareas
    # ----------------------------------------
    SI opcion == "7" ENTONCES
        Mostrar "Lista actual de tareas:"
        Mostrar lista_tareas
    FIN SI

    # ----------------------------------------
    # Opción 8: Salir
    # ----------------------------------------
    SI opcion == "8" ENTONCES
        opcion = "salir"
        Mostrar "Cerrando el Widget Flotante Pomodoro"
    FIN SI

FIN MIENTRAS

Mostrar "Programa finalizado"

FIN

Conclusión:
Este diseño representa la lógica inicial del programa Widget Flotante Pomodoro. El flowchart permite visualizar cómo fluye la interacción del usuario con las tareas, prioridades, botones y temporizador. El pseudocódigo traduce esa lógica a pasos claros y ordenados, facilitando su futura implementación en Python.
*********************************************************************************************************************************
