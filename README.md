Proyecto-Final-1400
Widget Flotante Pomodoro

Descripción del Proyecto
    El Widget Flotante Pomodoro es una aplicación desarrollada en Python utilizando Tkinter.
    Permite gestionar tareas y controlar sesiones de enfoque mediante la técnica Pomodoro.

    El sistema integra:
        - Gestión de tareas (agregar, eliminar, completar)
        - Prioridades (Alta, Media, Baja)
        - Temporizador con cuenta regresiva
        - Periodos de descanso automáticos
        - Mensajes dentro del widget
        - Interfaz flotante siempre visible

Integrantes
    - Thais Medina
    - Pedro Ibanez
    - Jesús Hernan (c)

Estructura del Programa
    Proyecto/
        main.py              -    lógica principal
        tareas.json         -    almacenamiento (no implementado completamente)
        pomodoroApp.py  - interfaz gráfica
        README.md

Funcionamiento del Sistema
    Inicio
        Crear ventana con Tkinter
        Configurar widget flotante (always on top)
        Mostrar interfaz

    Usuario puede:
        - Agregar tarea
        - Seleccionar tarea
        - Eliminar tarea
        - Iniciar temporizador
        - Pausar
        - Completar tarea

    Si el usuario inicia:
        Verificar que haya tarea seleccionada
        Verificar que el tiempo sea válido

        Si es válido:
            Convertir minutos a segundos
            Iniciar temporizador

    Mientras tiempo > 0:
        Actualizar cronómetro cada segundo usando after()

    Cuando tiempo termina:
        Mostrar mensaje dentro del widget
        Esperar acción del usuario

    Si tarea se completa:
        Marcar como completada
        Iniciar descanso automático

    Durante descanso:
        Ejecutar temporizador de descanso
        Mostrar mensaje correspondiente

    Fin

Pseudocódigo
    INICIO

        Crear lista de tareas

        Crear interfaz gráfica

        MIENTRAS programa activo

            SI usuario presiona "Agregar"
                Leer nombre
                Leer tiempo
                Leer prioridad

                SI datos válidos
                    Crear tarea
                    Guardar en lista
                    Actualizar interfaz
                SINO
                    Mostrar error
                FIN SI
            FIN SI

            SI usuario selecciona tarea
                Guardar índice seleccionado
            FIN SI

            SI usuario presiona "Eliminar"
                Verificar selección
                Eliminar tarea de lista
                Actualizar interfaz
            FIN SI

            SI usuario presiona "Comenzar"

                SI ya está corriendo
                    Mostrar mensaje
                SINO

                    SI hay tarea seleccionada

                        SI tiempo válido

                            tiempo_restante = tiempo * 60

                            MIENTRAS tiempo_restante > 0
                                Mostrar tiempo
                                Esperar 1 segundo (after)
                                tiempo_restante = tiempo_restante - 1
                            FIN MIENTRAS

                            Mostrar mensaje "Tiempo terminado"

                        SINO
                            Mostrar error
                        FIN SI

                    SINO
                        Mostrar mensaje "Selecciona tarea"
                    FIN SI

                FIN SI

            FIN SI

            SI usuario presiona "Pausar"
                Detener temporizador
            FIN SI

            SI usuario presiona "Completar"
                Marcar tarea como completada
                Iniciar descanso
            FIN SI

        FIN MIENTRAS

    FIN

Conceptos Aplicados
    - Condicionales (if / else)
    - Eventos de interfaz (botones)
    - Temporizador con after()
    - Manejo de listas y diccionarios
    - Programación orientada a objetos
    - Validación de datos del usuario

Decisiones Técnicas
    1. Uso de after() en lugar de while
        Evita que la interfaz se congele

    2. Separación por clases
        Pomodoro -> datos
        PomodoroApp -> interfaz y control

    3. Interfaz dinámica
        Se ocultan y muestran controles según el estado

    4. Colores por prioridad
        Alta -> rojo
        Media -> naranja
        Baja -> verde
        Completada -> gris

Requisitos
    - Python 3.x
    - Tkinter (incluido por defecto)

Conclusión
    Este proyecto implementa una aplicación funcional que integra
    interfaz gráfica, control de flujo y manejo de eventos.

    Demuestra la aplicación práctica de los conceptos aprendidos en clase
    y representa una solución real para la gestión del tiempo y tareas.

