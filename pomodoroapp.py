import tkinter as tk  # Librería para interfaz gráfica
import json           # Permite trabajar con archivos JSON
import os             # Permite verificar si el archivo existe


# BLOQUE 1: DATOS Y CONFIGURACIÓN
class Pomodoro:
    def __init__(self):
        self.archivo = "tareas.json"  # Nombre del archivo donde se guardan las tareas
        self.tareas = []  # Lista de tareas
        self.tiempo_restante = 0  # Tiempo restante del temporizador en segundos

    def cargar_tareas(self):
        # Verifica si el archivo JSON existe
        if os.path.exists(self.archivo):
            try:
                # Abre el archivo en modo lectura y carga las tareas
                with open(self.archivo, "r", encoding="utf-8") as f:
                    self.tareas = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.tareas = []
        else:
            self.tareas = []

    def guardar_tareas(self):
        try:
            # Guarda la lista de tareas en el archivo JSON
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(self.tareas, f, indent=4, ensure_ascii=False)
        except OSError:
            pass


# BLOQUE 2: INTERFAZ Y FUNCIONES DE TAREAS
class PomodoroApp:
    def __init__(self):
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Widget Pomodoro")
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        # Tamaño del widget
        self.root.geometry("360x780")

        # Crear objeto de datos
        self.pomodoro = Pomodoro()
        self.pomodoro.cargar_tareas()

        # Variables de control
        self.en_cuenta = False
        self.en_descanso = False
        self.tarea_actual = None
        self.trabajo_id = None

        # Variable para prioridad
        self.prioridad_var = tk.StringVar(value="Media")

        # Crear interfaz
        self.setup_ui()

        # Mostrar tareas cargadas
        self.mostrar_tareas()

    def setup_ui(self):
        self.marco = tk.Frame(self.root)
        self.marco.pack(padx=10, pady=10)

        # Entrada del nombre de la tarea
        tk.Label(self.marco, text="Tarea").pack()
        self.entrada = tk.Entry(self.marco, width=30)
        self.entrada.pack()

        # Entrada del tiempo de trabajo
        tk.Label(self.marco, text="Minutos de trabajo").pack()
        self.tiempo_entry = tk.Entry(self.marco, width=15)
        self.tiempo_entry.pack()

        # Entrada del tiempo de descanso
        tk.Label(self.marco, text="Minutos de descanso").pack()
        self.descanso_entry = tk.Entry(self.marco, width=15)
        self.descanso_entry.pack()
        self.descanso_entry.insert(0, "5")  # Descanso por defecto

        # Opciones de prioridad
        tk.Label(self.marco, text="Prioridad").pack(pady=(8, 0))

        self.frame_prioridad = tk.Frame(self.marco)
        self.frame_prioridad.pack()

        self.rb_alta = tk.Radiobutton(
            self.frame_prioridad,
            text="Alta",
            variable=self.prioridad_var,
            value="Alta"
        )
        self.rb_alta.pack(side="left", padx=5)

        self.rb_media = tk.Radiobutton(
            self.frame_prioridad,
            text="Media",
            variable=self.prioridad_var,
            value="Media"
        )
        self.rb_media.pack(side="left", padx=5)

        self.rb_baja = tk.Radiobutton(
            self.frame_prioridad,
            text="Baja",
            variable=self.prioridad_var,
            value="Baja"
        )
        self.rb_baja.pack(side="left", padx=5)

        # Lista de tareas
        self.lista = tk.Listbox(self.marco, width=42, height=10)
        self.lista.pack(pady=8)

        # Botones de acciones
        tk.Button(self.marco, text="Agregar", command=self.agregar).pack(pady=2)
        tk.Button(self.marco, text="Comenzar", command=self.iniciar).pack(pady=2)
        tk.Button(self.marco, text="Pausar", command=self.pausar).pack(pady=2)
        tk.Button(self.marco, text="Completar", command=self.completar).pack(pady=2)
        tk.Button(self.marco, text="Eliminar", command=self.eliminar).pack(pady=2)
        tk.Button(self.marco, text="Reiniciar tareas", command=self.reiniciar_tareas).pack(pady=2)

        # Cronómetro
        self.timer_label = tk.Label(self.marco, text="00:00", font=("Arial", 20, "bold"))
        self.timer_label.pack(pady=8)

        # Mensajes dentro del widget
        self.mensaje = tk.Label(self.marco, text="", wraplength=300, justify="center")
        self.mensaje.pack(pady=4)

        # Felicitación dentro del widget
        self.felicitacion = tk.Label(
            self.marco,
            text="",
            fg="blue",
            font=("Arial", 11, "bold"),
            wraplength=300,
            justify="center"
        )
        self.felicitacion.pack(pady=4)

        # Botón salir
        tk.Button(self.marco, text="Salir", command=self.salir).pack(pady=6)

    def mostrar_tareas(self):
        # Limpia la lista antes de volver a mostrar las tareas
        self.lista.delete(0, tk.END)

        for tarea in self.pomodoro.tareas:
            estado = "✔" if tarea["completada"] else "✗"
            prioridad = tarea.get("prioridad", "Media")
            texto = f"{tarea['nombre']} - {tarea['tiempo']} min - {prioridad} - {estado}"
            self.lista.insert(tk.END, texto)

            ultimo = self.lista.size() - 1

            # Colorear según estado o prioridad
            if tarea["completada"]:
                self.lista.itemconfig(ultimo, fg="gray")
            elif prioridad == "Alta":
                self.lista.itemconfig(ultimo, fg="red")
            elif prioridad == "Media":
                self.lista.itemconfig(ultimo, fg="orange")
            else:
                self.lista.itemconfig(ultimo, fg="green")

        # Revisar si todas las tareas están completas
        self.verificar_felicitacion()

    def verificar_felicitacion(self):
        # Mostrar felicitación solo si hay tareas y todas están completadas
        if len(self.pomodoro.tareas) > 0 and all(t["completada"] for t in self.pomodoro.tareas):
            self.felicitacion.config(
                text="¡Felicitaciones! Has cumplido con todas tus tareas. Te has ganado una recompensa."
            )
        else:
            self.felicitacion.config(text="")

    def agregar(self):
        nombre = self.entrada.get().strip()
        tiempo = self.tiempo_entry.get().strip()
        prioridad = self.prioridad_var.get()

        # Validar datos obligatorios
        if nombre == "" or tiempo == "":
            self.mensaje.config(text="Datos incompletos.")
            return

        try:
            tiempo = int(tiempo)
            if tiempo <= 0:
                self.mensaje.config(text="El tiempo debe ser mayor que 0.")
                return
        except ValueError:
            self.mensaje.config(text="Tiempo inválido.")
            return

        # Crear nueva tarea
        tarea = {
            "nombre": nombre,
            "tiempo": tiempo,
            "prioridad": prioridad,
            "completada": False
        }

        # Guardar tarea
        self.pomodoro.tareas.append(tarea)
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()

        # Limpiar entradas
        self.entrada.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)
        self.prioridad_var.set("Media")
        self.mensaje.config(text="Tarea agregada correctamente.")

    def eliminar(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para eliminar.")
            return

        indice = seleccion[0]

        # Si se elimina la tarea actual, detener el temporizador
        if self.tarea_actual == indice:
            self.en_cuenta = False
            self.en_descanso = False
            self.pomodoro.tiempo_restante = 0
            self.tarea_actual = None

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.timer_label.config(text="00:00")

        self.pomodoro.tareas.pop(indice)
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()
        self.mensaje.config(text="Tarea eliminada.")

    def completar(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para completar.")
            return

        indice = seleccion[0]

        # Marcar tarea como completada
        self.pomodoro.tareas[indice]["completada"] = True
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()
        self.mensaje.config(text="Tarea completada.")

        # Si la tarea completada es la actual, iniciar descanso automático
        if self.tarea_actual == indice:
            self.en_cuenta = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.iniciar_descanso()

    def reiniciar_tareas(self):
        # Reiniciar todas las tareas a no completadas
        for tarea in self.pomodoro.tareas:
            tarea["completada"] = False

        # Reiniciar temporizadores y estado
        self.en_cuenta = False
        self.en_descanso = False
        self.pomodoro.tiempo_restante = 0
        self.tarea_actual = None

        if self.trabajo_id is not None:
            try:
                self.root.after_cancel(self.trabajo_id)
            except Exception:
                pass
            self.trabajo_id = None

        self.timer_label.config(text="00:00")
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()
        self.mensaje.config(text="Todas las tareas fueron reiniciadas.")

    # BLOQUE 3: TEMPORIZADOR Y EJECUCIÓN
    def actualizar_cronometro(self):
        minutos = self.pomodoro.tiempo_restante // 60
        segundos = self.pomodoro.tiempo_restante % 60
        self.timer_label.config(text=f"{minutos:02}:{segundos:02}")

    def iniciar(self):
        # Evitar iniciar si ya está corriendo
        if self.en_cuenta:
            self.mensaje.config(text="El temporizador ya está corriendo.")
            return

        # No iniciar si está en descanso
        if self.en_descanso:
            self.mensaje.config(text="Ahora mismo estás en descanso.")
            return

        # Reanudar si estaba pausado
        if self.pomodoro.tiempo_restante > 0 and self.tarea_actual is not None:
            self.en_cuenta = True
            self.mensaje.config(text="Temporizador reanudado.")
            self.contar()
            return

        seleccion = self.lista.curselection()
        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea.")
            return

        indice = seleccion[0]
        tarea = self.pomodoro.tareas[indice]

        if tarea["completada"]:
            self.mensaje.config(text="Esa tarea ya está completada.")
            return

        self.tarea_actual = indice
        self.pomodoro.tiempo_restante = tarea["tiempo"] * 60
        self.en_cuenta = True
        self.mensaje.config(text=f"Trabajando en: {tarea['nombre']}")
        self.contar()

    def pausar(self):
        if self.en_cuenta:
            self.en_cuenta = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.mensaje.config(text="Temporizador pausado.")
            return

        if self.en_descanso:
            self.en_descanso = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except Exception:
                    pass
                self.trabajo_id = None

            self.mensaje.config(text="Descanso pausado.")
            return

        self.mensaje.config(text="No hay temporizador activo.")

    def contar(self):
        # Ejecutar temporizador de trabajo
        if self.en_cuenta and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar)
            return

        # Cuando termina el tiempo de trabajo
        if self.en_cuenta and self.pomodoro.tiempo_restante <= 0:
            self.en_cuenta = False
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.trabajo_id = None
            self.mensaje.config(text="Tiempo terminado. La tarea se marcará como completada.")

            # Completar automáticamente la tarea actual
            if self.tarea_actual is not None:
                self.pomodoro.tareas[self.tarea_actual]["completada"] = True
                self.pomodoro.guardar_tareas()
                self.mostrar_tareas()

            # Iniciar descanso automáticamente
            self.iniciar_descanso()

    def iniciar_descanso(self):
        # Leer minutos de descanso
        try:
            descanso = int(self.descanso_entry.get().strip())
            if descanso <= 0:
                descanso = 5
        except ValueError:
            descanso = 5

        self.en_descanso = True
        self.tarea_actual = None
        self.pomodoro.tiempo_restante = descanso * 60
        self.actualizar_cronometro()
        self.mensaje.config(text=f"Descanso en curso: {descanso} minutos.")
        self.contar_descanso()

    def contar_descanso(self):
        # Ejecutar temporizador de descanso
        if self.en_descanso and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar_descanso)
            return

        # Cuando termina el descanso
        if self.en_descanso and self.pomodoro.tiempo_restante <= 0:
            self.en_descanso = False
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.trabajo_id = None
            self.mensaje.config(text="Descanso terminado. Selecciona la siguiente tarea.")

    def salir(self):
        if self.trabajo_id is not None:
            try:
                self.root.after_cancel(self.trabajo_id)
            except Exception:
                pass

        self.pomodoro.guardar_tareas()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
