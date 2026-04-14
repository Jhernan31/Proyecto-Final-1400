import tkinter as tk  # Librería para crear la interfaz gráfica


#BLOQUE 1: CONFIGURACIÓN E INTERFAZ 

class Pomodoro:
    def __init__(self):
        self.archivo = "tareas.json"  # Nombre del archivo para guardar tareas
        self.tareas = []  # Lista de tareas
        self.tiempo_restante = 0  # Tiempo restante del temporizador en segundos


class PomodoroApp:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Widget Pomodoro")
        self.root.attributes("-topmost", True)  # Mantener ventana al frente
        self.root.protocol("WM_DELETE_WINDOW", self.salir)  # Cerrar correctamente

        # Definir tamaño de ventana
        ancho = 320
        alto = 650

        # Obtener tamaño de pantalla
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        # Calcular posición centrada
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        # Aplicar tamaño y posición
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Crear el objeto que guarda los datos
        self.pomodoro = Pomodoro()

        # Variables para controlar el temporizador
        self.en_cuenta = False  # Indica si el temporizador está corriendo
        self.en_descanso = False  # Indica si está en descanso
        self.tarea_actual = None  # Guarda el índice de la tarea actual
        self.trabajo_id = None  # Guarda el ID del método after()

        # Crear la interfaz
        self.setup_ui()

        # Mostrar tareas al iniciar
        self.mostrar_tareas()

    def setup_ui(self):
        # Crear el marco principal
        self.marco = tk.Frame(self.root, bd=2, relief="solid")
        self.marco.pack(fill="both", expand=True, padx=8, pady=8)

        # Título principal
        self.titulo = tk.Label(self.marco, text="Widget Pomodoro", font=("Arial", 14, "bold"))
        self.titulo.pack(pady=4)

        # Campo para el nombre de la tarea
        self.label_nombre = tk.Label(self.marco, text="Nombre de la tarea")
        self.label_nombre.pack()

        self.entrada = tk.Entry(self.marco, width=28)
        self.entrada.pack(pady=3)

        # Campo para el tiempo en minutos
        self.label_tiempo = tk.Label(self.marco, text="Tiempo en minutos")
        self.label_tiempo.pack()

        self.tiempo_entry = tk.Entry(self.marco, width=10)
        self.tiempo_entry.pack(pady=3)

        # Campo para el descanso
        self.label_descanso = tk.Label(self.marco, text="Descanso en minutos")
        self.label_descanso.pack()

        self.descanso_entry = tk.Entry(self.marco, width=10)
        self.descanso_entry.insert(0, "5")  # Valor por defecto
        self.descanso_entry.pack(pady=3)

        # Opción de prioridad
        self.label_prioridad = tk.Label(self.marco, text="Prioridad")
        self.label_prioridad.pack()

        self.prioridad_var = tk.StringVar(value="Media")
        self.frame_prioridad = tk.Frame(self.marco)
        self.frame_prioridad.pack(pady=3)

        self.rb_alta = tk.Radiobutton(
            self.frame_prioridad, text="Alta",
            variable=self.prioridad_var, value="Alta"
        )
        self.rb_alta.pack(side="left")

        self.rb_media = tk.Radiobutton(
            self.frame_prioridad, text="Media",
            variable=self.prioridad_var, value="Media"
        )
        self.rb_media.pack(side="left")

        self.rb_baja = tk.Radiobutton(
            self.frame_prioridad, text="Baja",
            variable=self.prioridad_var, value="Baja"
        )
        self.rb_baja.pack(side="left")

        # Botón para agregar tareas
        self.boton_agregar = tk.Button(self.marco, text="Agregar tarea", command=self.agregar)
        self.boton_agregar.pack(pady=4)

        # Etiqueta y lista de tareas
        self.label_seleccionar = tk.Label(self.marco, text="Seleccionar tarea")
        self.label_seleccionar.pack()

        self.lista = tk.Listbox(self.marco, height=5, width=35)
        self.lista.pack(pady=4)

        # Botones de acciones
        self.boton_comenzar = tk.Button(self.marco, text="Comenzar", command=self.iniciar)
        self.boton_comenzar.pack(pady=3)

        self.boton_pausar = tk.Button(self.marco, text="Pausar", command=self.pausar)
        self.boton_pausar.pack(pady=3)

        self.boton_completar = tk.Button(self.marco, text="Completar tarea", command=self.completar)
        self.boton_completar.pack(pady=3)

        self.boton_eliminar = tk.Button(self.marco, text="Eliminar tarea", command=self.eliminar)
        self.boton_eliminar.pack(pady=3)

        # Etiqueta del cronómetro
        self.label_cronometro = tk.Label(self.marco, text="Cronómetro")
        self.label_cronometro.pack(pady=(6, 0))

        self.timer_label = tk.Label(self.marco, text="00:00", font=("Arial", 20, "bold"))
        self.timer_label.pack(pady=2)

        # Etiqueta para mostrar mensajes
        self.mensaje = tk.Label(self.marco, text="", wraplength=280, justify="center")
        self.mensaje.pack(pady=2)

        # Botón para salir
        self.boton_salir = tk.Button(self.marco, text="Salir", command=self.salir)
        self.boton_salir.pack(pady=2)


# BLOQUE 2: GESTIÓN DE TAREAS

    def mostrar_tareas(self):
        # Limpiar la lista antes de volver a mostrarla
        self.lista.delete(0, tk.END)

        # Recorrer todas las tareas guardadas
        for tarea in self.pomodoro.tareas:
            estado = "Completada" if tarea["completada"] else "Pendiente"
            texto = f"{tarea['nombre']} | {tarea['tiempo']} min | {tarea['prioridad']} | {estado}"
            self.lista.insert(tk.END, texto)

            # Obtener la última posición insertada
            ultimo = self.lista.size() - 1

            # Cambiar color según estado o prioridad
            if tarea["completada"]:
                self.lista.itemconfig(ultimo, fg="gray")
            elif tarea["prioridad"] == "Alta":
                self.lista.itemconfig(ultimo, fg="red")
            elif tarea["prioridad"] == "Media":
                self.lista.itemconfig(ultimo, fg="orange")
            else:
                self.lista.itemconfig(ultimo, fg="green")

    def agregar(self):
        # Obtener nombre, tiempo y prioridad
        nombre = self.entrada.get().strip()
        tiempo = self.tiempo_entry.get().strip()
        prioridad = self.prioridad_var.get()

        # Validar que los campos no estén vacíos
        if nombre == "" or tiempo == "":
            self.mensaje.config(text="Escribe la tarea y el tiempo.")
            return

        # Validar que el tiempo sea entero
        try:
            tiempo = int(tiempo)
            if tiempo <= 0:
                self.mensaje.config(text="El tiempo debe ser mayor que 0.")
                return
        except ValueError:
            self.mensaje.config(text="El tiempo debe ser un número entero.")
            return

        # Crear diccionario con la nueva tarea
        nueva_tarea = {
            "nombre": nombre,
            "tiempo": tiempo,
            "prioridad": prioridad,
            "completada": False
        }

        # Guardar tarea en la lista
        self.pomodoro.tareas.append(nueva_tarea)

        # Actualizar la vista
        self.mostrar_tareas()

        # Limpiar campos
        self.entrada.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)
        self.prioridad_var.set("Media")
        self.mensaje.config(text="")

    def eliminar(self):
        # Obtener tarea seleccionada
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para eliminar.")
            return

        indice = seleccion[0]

        # Si la tarea eliminada es la actual, detener temporizador
        if self.tarea_actual == indice:
            self.en_cuenta = False
            self.pomodoro.tiempo_restante = 0
            self.tarea_actual = None

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.timer_label.config(text="00:00")

        # Eliminar la tarea
        self.pomodoro.tareas.pop(indice)
        self.mostrar_tareas()
        self.mensaje.config(text="")

    def completar(self):
        # Obtener tarea seleccionada
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para completar.")
            return

        indice = seleccion[0]

        # Marcar la tarea como completada
        self.pomodoro.tareas[indice]["completada"] = True
        self.mostrar_tareas()

        # Si es la tarea que estaba corriendo, detener el trabajo
        if self.tarea_actual == indice:
            self.en_cuenta = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            # Leer el tiempo de descanso
            try:
                descanso = int(self.descanso_entry.get())
                if descanso <= 0:
                    descanso = 5
            except ValueError:
                descanso = 5

            # Iniciar descanso
            self.en_descanso = True
            self.pomodoro.tiempo_restante = descanso * 60
            self.tarea_actual = None
            self.actualizar_cronometro()
            self.mensaje.config(text=f"Descanso: {descanso} minutos")
            self.contar_descanso()
        else:
            self.mensaje.config(text="")


# BLOQUE 3: TEMPORIZADOR Y EJECUCIÓN

    def actualizar_cronometro(self):
        # Convertir segundos en minutos y segundos
        minutos = self.pomodoro.tiempo_restante // 60
        segundos = self.pomodoro.tiempo_restante % 60

        # Mostrar el tiempo con dos dígitos
        self.timer_label.config(text=f"{minutos:02}:{segundos:02}")

    def iniciar(self):
        # Evitar iniciar si ya está corriendo
        if self.en_cuenta:
            self.mensaje.config(text="El temporizador ya está corriendo.")
            return

        # No permitir iniciar durante descanso
        if self.en_descanso:
            self.mensaje.config(text="Ahora mismo estás en descanso.")
            return

        # Reanudar si estaba pausado
        if self.pomodoro.tiempo_restante > 0 and self.tarea_actual is not None:
            self.en_cuenta = True
            nombre = self.pomodoro.tareas[self.tarea_actual]["nombre"]
            self.mensaje.config(text=f"Reanudando: {nombre}")
            self.contar()
            return

        # Obtener tarea seleccionada
        seleccion = self.lista.curselection()
        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea antes de comenzar.")
            return

        indice = seleccion[0]
        tarea = self.pomodoro.tareas[indice]

        # No iniciar tareas ya completadas
        if tarea["completada"]:
            self.mensaje.config(text="Esa tarea ya está completada.")
            return

        # Convertir minutos a segundos e iniciar
        self.tarea_actual = indice
        self.pomodoro.tiempo_restante = tarea["tiempo"] * 60
        self.actualizar_cronometro()
        self.en_cuenta = True
        self.mensaje.config(text=f"Trabajando en: {tarea['nombre']}")
        self.contar()

    def pausar(self):
        # Pausar el temporizador de trabajo
        if self.en_cuenta:
            self.en_cuenta = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.mensaje.config(text="Temporizador pausado.")

        # Pausar el descanso
        elif self.en_descanso:
            self.en_descanso = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.mensaje.config(text="Descanso pausado.")
        else:
            self.mensaje.config(text="No hay temporizador en marcha.")

    def contar(self):
        # Mientras el temporizador esté activo y quede tiempo
        if self.en_cuenta and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1

            # Llamar esta misma función después de 1 segundo
            self.trabajo_id = self.root.after(1000, self.contar)

        elif self.pomodoro.tiempo_restante <= 0 and self.en_cuenta:
            # Al terminar el tiempo, detener el temporizador
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.en_cuenta = False
            self.trabajo_id = None
            self.mensaje.config(text="Tiempo terminado. Marca la tarea como completada.")
            self.tarea_actual = None

    def contar_descanso(self):
        # Mientras el descanso esté activo y quede tiempo
        if self.en_descanso and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1

            # Llamar esta función otra vez en 1 segundo
            self.trabajo_id = self.root.after(1000, self.contar_descanso)

        elif self.en_descanso and self.pomodoro.tiempo_restante <= 0:
            # Al terminar el descanso, volver a estado normal
            self.en_descanso = False
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.trabajo_id = None
            self.mensaje.config(text="Descanso terminado. Selecciona la siguiente tarea.")

    def salir(self):
        # Cancelar temporizador si estaba programado
        self.en_cuenta = False
        self.en_descanso = False

        if self.trabajo_id is not None:
            try:
                self.root.after_cancel(self.trabajo_id)
            except Exception:
                pass
            self.trabajo_id = None

        # Cerrar la aplicación
        self.root.quit()
        self.root.destroy()

    def run(self):
        # Mantener la ventana abierta
        self.root.mainloop()


# Crear la aplicación
app = PomodoroApp()

# Ejecutar el programa
app.run()
