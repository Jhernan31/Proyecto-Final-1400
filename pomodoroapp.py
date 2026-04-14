import tkinter as tk
import json
import os


# BLOQUE 1: DATOS Y CONFIGURACIÓN
class Pomodoro:
    def __init__(self):
        self.archivo = "tareas.json"  # Archivo JSON donde se guardan las tareas
        self.tareas = []  # Lista de tareas
        self.tiempo_restante = 0  # Tiempo restante en segundos

    def cargar_tareas(self):
        # Carga las tareas desde el archivo JSON si existe
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    self.tareas = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.tareas = []
        else:
            self.tareas = []

    def guardar_tareas(self):
        # Guarda las tareas en el archivo JSON
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(self.tareas, f, indent=4, ensure_ascii=False)
        except OSError:
            pass


# BLOQUE 2: INTERFAZ Y TAREAS
class PomodoroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Widget Pomodoro")
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        # Ventana más compacta
        self.root.geometry("380x640")
        self.root.resizable(False, False)

        self.pomodoro = Pomodoro()
        self.pomodoro.cargar_tareas()

        self.en_cuenta = False
        self.en_descanso = False
        self.tarea_actual = None
        self.trabajo_id = None

        self.prioridad_var = tk.StringVar(value="Media")

        self.setup_ui()
        self.mostrar_tareas()

    def setup_ui(self):
        self.marco = tk.Frame(self.root, padx=10, pady=10)
        self.marco.pack(fill="both", expand=True)

        tk.Label(self.marco, text="Widget Pomodoro", font=("Arial", 14, "bold")).pack(pady=(0, 8))

        tk.Label(self.marco, text="Tarea").pack()
        self.entrada = tk.Entry(self.marco, width=30)
        self.entrada.pack(pady=(0, 6))

        tk.Label(self.marco, text="Minutos de trabajo").pack()
        self.tiempo_entry = tk.Entry(self.marco, width=15)
        self.tiempo_entry.pack(pady=(0, 6))

        tk.Label(self.marco, text="Minutos de descanso").pack()
        self.descanso_entry = tk.Entry(self.marco, width=15)
        self.descanso_entry.pack(pady=(0, 8))
        self.descanso_entry.insert(0, "5")

        tk.Label(self.marco, text="Prioridad").pack()

        self.frame_prioridad = tk.Frame(self.marco)
        self.frame_prioridad.pack(pady=(0, 8))

        tk.Radiobutton(
            self.frame_prioridad,
            text="Alta",
            variable=self.prioridad_var,
            value="Alta"
        ).pack(side="left", padx=6)

        tk.Radiobutton(
            self.frame_prioridad,
            text="Media",
            variable=self.prioridad_var,
            value="Media"
        ).pack(side="left", padx=6)

        tk.Radiobutton(
            self.frame_prioridad,
            text="Baja",
            variable=self.prioridad_var,
            value="Baja"
        ).pack(side="left", padx=6)

        self.lista = tk.Listbox(self.marco, width=42, height=8)
        self.lista.pack(pady=(0, 8))

        self.frame_botones = tk.Frame(self.marco)
        self.frame_botones.pack(pady=(0, 8))

        tk.Button(self.frame_botones, text="Agregar", width=14, command=self.agregar).grid(row=0, column=0, padx=4, pady=2)
        tk.Button(self.frame_botones, text="Comenzar", width=14, command=self.iniciar).grid(row=0, column=1, padx=4, pady=2)
        tk.Button(self.frame_botones, text="Pausar", width=14, command=self.pausar).grid(row=1, column=0, padx=4, pady=2)
        tk.Button(self.frame_botones, text="Completar", width=14, command=self.completar).grid(row=1, column=1, padx=4, pady=2)
        tk.Button(self.frame_botones, text="Eliminar", width=14, command=self.eliminar).grid(row=2, column=0, padx=4, pady=2)
        tk.Button(self.frame_botones, text="Reiniciar tareas", width=14, command=self.reiniciar_tareas).grid(row=2, column=1, padx=4, pady=2)

        self.timer_label = tk.Label(self.marco, text="00:00", font=("Arial", 22, "bold"))
        self.timer_label.pack(pady=(4, 6))

        self.mensaje = tk.Label(self.marco, text="", wraplength=320, justify="center")
        self.mensaje.pack(pady=(0, 6))

        self.felicitacion = tk.Label(
            self.marco,
            text="",
            fg="blue",
            font=("Arial", 10, "bold"),
            wraplength=320,
            justify="center"
        )
        self.felicitacion.pack(pady=(0, 8))

        tk.Button(self.marco, text="Salir", width=14, command=self.salir).pack()

    def mostrar_tareas(self):
        self.lista.delete(0, tk.END)

        for tarea in self.pomodoro.tareas:
            estado = "✔" if tarea["completada"] else "✗"
            prioridad = tarea.get("prioridad", "Media")
            texto = f"{tarea['nombre']} - {tarea['tiempo']} min - {prioridad} - {estado}"
            self.lista.insert(tk.END, texto)

            ultimo = self.lista.size() - 1

            if tarea["completada"]:
                self.lista.itemconfig(ultimo, fg="gray")
            elif prioridad == "Alta":
                self.lista.itemconfig(ultimo, fg="red")
            elif prioridad == "Media":
                self.lista.itemconfig(ultimo, fg="orange")
            else:
                self.lista.itemconfig(ultimo, fg="green")

        self.verificar_felicitacion()

    def verificar_felicitacion(self):
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

        if nombre == "" or tiempo == "":
            self.mensaje.config(text="Escribe la tarea y el tiempo.")
            return

        try:
            tiempo = int(tiempo)
            if tiempo <= 0:
                self.mensaje.config(text="El tiempo debe ser mayor que 0.")
                return
        except ValueError:
            self.mensaje.config(text="El tiempo debe ser un número entero.")
            return

        tarea = {
            "nombre": nombre,
            "tiempo": tiempo,
            "prioridad": prioridad,
            "completada": False
        }

        self.pomodoro.tareas.append(tarea)
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()

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

        if self.tarea_actual == indice:
            self.detener_temporizador()

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
        self.pomodoro.tareas[indice]["completada"] = True
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()
        self.mensaje.config(text="Tarea completada.")

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
        for tarea in self.pomodoro.tareas:
            tarea["completada"] = False

        self.detener_temporizador()
        self.pomodoro.guardar_tareas()
        self.mostrar_tareas()
        self.mensaje.config(text="Todas las tareas fueron reiniciadas.")

    def detener_temporizador(self):
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

    # BLOQUE 3: TEMPORIZADOR Y MENSAJES
    def actualizar_cronometro(self):
        minutos = self.pomodoro.tiempo_restante // 60
        segundos = self.pomodoro.tiempo_restante % 60
        self.timer_label.config(text=f"{minutos:02}:{segundos:02}")

    def iniciar(self):
        if self.en_cuenta:
            self.mensaje.config(text="El temporizador ya está corriendo.")
            return

        if self.en_descanso:
            self.mensaje.config(text="Ahora mismo estás en descanso.")
            return

        if self.pomodoro.tiempo_restante > 0 and self.tarea_actual is not None:
            self.en_cuenta = True
            nombre = self.pomodoro.tareas[self.tarea_actual]["nombre"]
            self.mensaje.config(text=f"Reanudando: {nombre}")
            self.contar()
            return

        seleccion = self.lista.curselection()
        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea antes de comenzar.")
            return

        indice = seleccion[0]
        tarea = self.pomodoro.tareas[indice]

        if tarea["completada"]:
            self.mensaje.config(text="Esa tarea ya está completada.")
            return

        self.tarea_actual = indice
        self.pomodoro.tiempo_restante = tarea["tiempo"] * 60
        self.en_cuenta = True
        self.actualizar_cronometro()
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
        if self.en_cuenta and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar)
            return

        if self.en_cuenta and self.pomodoro.tiempo_restante <= 0:
            self.en_cuenta = False
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.trabajo_id = None

            if self.tarea_actual is not None:
                self.pomodoro.tareas[self.tarea_actual]["completada"] = True
                self.pomodoro.guardar_tareas()
                self.mostrar_tareas()

            self.mensaje.config(text="Tiempo terminado. Iniciando descanso automático.")
            self.iniciar_descanso()

    def iniciar_descanso(self):
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
        if self.en_descanso and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar_descanso)
            return

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
