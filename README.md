Widget Flotante Pomodoro
Descripción del Proyecto

El Widget Flotante Pomodoro es una aplicación desarrollada en Python con Tkinter que permite al usuario organizar tareas y gestionar sesiones de enfoque utilizando la técnica Pomodoro.

El sistema incluye:
Gestión de tareas
Asignación de prioridades
Temporizador con cuenta regresiva
Control del tiempo (pausar, reiniciar)
Marcado y eliminación de tareas
Mensajes motivacionales al finalizar

Presentación del Proyecto
 Parte 1 – Thais Medina

Diseño del Sistema y Experiencia del Usuario
El sistema fue diseñado para ser intuitivo y fácil de usar, permitiendo al usuario interactuar mediante botones y entradas simples.

Funcionalidades implementadas:
#Gestión de tareas
#Agregar tareas mediante un campo de texto
#Seleccionar prioridad (Alta, Media, Baja)
#Visualización en lista
#Prioridades por color
Alta → rojo
Media → naranja
Baja → verde
Esto permite identificar rápidamente la importancia de cada tarea.

Parte 2 – Pedro
Lógica del Sistema y Estructura
El programa utiliza estructuras de datos y control de flujo para manejar el comportamiento del sistema.
#Estructuras utilizadas:
#Lista de tareas (tareas)
#Diccionarios para almacenar nombre, prioridad y estado

#Condicionales implementados:
Validación de tarea vacía
Validación de prioridad
Validación de tiempo ingresado
Verificación de finalización del temporizador
#Bucle del temporizador:
Se implementa mediante after() de Tkinter, simulando:
while tiempo_restante > 0:
Esto permite actualizar la interfaz sin bloquear el programa.

Parte 3 – Jesús
Funcionalidad Avanzada y Control del Sistema
#Temporizador
#Inicia con minutos ingresados
#Convierte a segundos
#Realiza cuenta regresiva
#Controles del temporizador
Pausar → detiene el contador
Reiniciar → vuelve a 00:00

#Gestión de tareas
Completar tarea → cambia estado y color
Eliminar tarea → la remueve de la lista
Mensaje motivacional

Al finalizar el tiempo, el sistema muestra:

“¡Tiempo terminado! Excelente trabajo. Te has ganado una recompensa 

Esto mejora la experiencia del usuario.

TODOS - Flujo del Programa 

1. Inicialización
Se crean variables:lista de tareas, temporizador, estado del sistema

2. Interfaz
Se muestra ventana flotante, Usuario interactúa con botones

3. Rutas principales
Agregar tarea
Usuario escribe tarea
Selecciona prioridad
Sistema valida datos
Se asigna color
Se guarda en la lista

Iniciar temporizador
Seleccionar tarea

Ingresar tiempo
Validar tiempo
Iniciar cuenta regresiva
Mientras el tiempo > 0:
Mostrar tiempo

Esperar 1 segundo
Reducir contador

Al finalizar:

Mostrar mensaje
Permitir completar tarea

Nueva sesión
Usuario puede repetir el proceso

O salir del sistema

Pseudocódigo (Adaptado a implementación)
INICIO

Crear lista tareas
Crear temporizador

MIENTRAS aplicación activa

    SI usuario agrega tarea
        validar datos
        guardar tarea

    SI usuario inicia temporizador
        validar tiempo
        iniciar cuenta regresiva

    SI usuario pausa
        detener temporizador

    SI usuario reinicia
        resetear tiempo

    SI usuario completa tarea
        marcar como completada

    SI usuario elimina tarea
        borrar tarea

FIN

Mostrar mensaje final

FIN

Tecnologías utilizadas
Python 3
Tkinter

Estructura del proyecto
proyecto-final-1400/
main.
pomodor_widget.py
README.md
imagen_diagrama_de_flujo

Autores
Thais Medina,
Pedro Ibanez y 
Jesús Hernan

Conclusión

Este proyecto demuestra la implementación completa de un sistema interactivo basado en la técnica Pomodoro, integrando diseño lógico (flowchart), pseudocódigo y desarrollo en Python.



El resultado es una aplicación funcional que combina organización, control del tiempo y experiencia de usuario
