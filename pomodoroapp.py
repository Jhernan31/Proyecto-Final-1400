import tkinter as tk
# import json
# import os

#BLOQUE 1: INTRODUCCIÓN DE VARIABLES Y VENTANA
class Pomodoro:
    def __init__(self):
        self.archivo = "tareas.json"
        self.tareas = []
        self.tiempo_restante = 0


class PomodoroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Widget Pomodoro")
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

        ancho = 320
        alto = 650

        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.pomodoro = Pomodoro()
        self.en_cuenta = False
        self.en_descanso = False
        self.tarea_actual = None
        self.trabajo_id = None

        self.setup_ui()
        self.mostrar_tareas()

    def setup_ui(self):
        self.marco = tk.Frame(self.root, bd=2, relief="solid")
        self.marco.pack(fill="both", expand=True, padx=8, pady=8)

        self.titulo = tk.Label(
            self.marco,
            text="Widget Pomodoro",
            font=("Arial", 14, "bold")
        )
        self.titulo.pack(pady=4)

        self.label_nombre = tk.Label(self.marco, text="Nombre de la tarea")
        self.label_nombre.pack()

        self.entrada = tk.Entry(self.marco, width=28)
        self.entrada.pack(pady=3)

        self.label_tiempo = tk.Label(self.marco, text="Tiempo en minutos")
        self.label_tiempo.pack()

        self.tiempo_entry = tk.Entry(self.marco, width=10)
        self.tiempo_entry.pack(pady=3)

        self.label_descanso = tk.Label(self.marco, text="Descanso en minutos")
        self.label_descanso.pack()

        self.descanso_entry = tk.Entry(self.marco, width=10)
        self.descanso_entry.insert(0, "5")
        self.descanso_entry.pack(pady=3)

        self.label_prioridad = tk.Label(self.marco, text="Prioridad")
        self.label_prioridad.pack()

        self.prioridad_var = tk.StringVar(value="Media")
        self.frame_prioridad = tk.Frame(self.marco)
        self.frame_prioridad.pack(pady=3)

        self.rb_alta = tk.Radiobutton(
            self.frame_prioridad,
            text="Alta",
            variable=self.prioridad_var,
            value="Alta"
        )
        self.rb_alta.pack(side="left")

        self.rb_media = tk.Radiobutton(
            self.frame_prioridad,
            text="Media",
            variable=self.prioridad_var,
            value="Media"
        )
        self.rb_media.pack(side="left")

        self.rb_baja = tk.Radiobutton(
            self.frame_prioridad,
            text="Baja",
            variable=self.prioridad_var,
            value="Baja"
        )
        self.rb_baja.pack(side="left")

        self.boton_agregar = tk.Button(
            self.marco,
            text="Agregar tarea",
            command=self.agregar
        )
        self.boton_agregar.pack(pady=4)

        self.label_seleccionar = tk.Label(self.marco, text="Seleccionar tarea")
        self.label_seleccionar.pack()

        self.lista = tk.Listbox(self.marco, height=5, width=35)
        self.lista.pack(pady=4)

        self.boton_comenzar = tk.Button(
            self.marco,
            text="Comenzar",
            command=self.iniciar
        )
        self.boton_comenzar.pack(pady=3)

        self.boton_pausar = tk.Button(
            self.marco,
            text="Pausar",
            command=self.pausar
        )
        self.boton_pausar.pack(pady=3)

        self.boton_completar = tk.Button(
            self.marco,
            text="Completar tarea",
            command=self.completar
        )
        self.boton_completar.pack(pady=3)

        self.boton_eliminar = tk.Button(
            self.marco,
            text="Eliminar tarea",
            command=self.eliminar
        )
        self.boton_eliminar.pack(pady=3)

        self.label_cronometro = tk.Label(self.marco, text="Cronómetro")
        self.label_cronometro.pack(pady=(6, 0))

        self.timer_label = tk.Label(
            self.marco,
            text="00:00",
            font=("Arial", 20, "bold")
        )
        self.timer_label.pack(pady=2)

        self.mensaje = tk.Label(
            self.marco,
            text="",
            wraplength=280,
            justify="center"
        )
        self.mensaje.pack(pady=2)

        self.boton_salir = tk.Button(
            self.marco,
            text="Salir",
            command=self.salir
        )
        self.boton_salir.pack(pady=2)
        
    #BLOQUE 2: CONTROL DEL TEMPORIZADOR
    def ocultar_controles(self):
        self.titulo.pack_forget()
        self.label_nombre.pack_forget()
        self.entrada.pack_forget()
        self.label_tiempo.pack_forget()
        self.tiempo_entry.pack_forget()
        self.label_descanso.pack_forget()
        self.descanso_entry.pack_forget()
        self.label_prioridad.pack_forget()
        self.frame_prioridad.pack_forget()
        self.boton_agregar.pack_forget()
        self.label_seleccionar.pack_forget()
        self.lista.pack_forget()
        self.boton_comenzar.pack_forget()
        self.boton_completar.pack_forget()
        self.boton_eliminar.pack_forget()
        self.label_cronometro.pack_forget()

        self.timer_label.pack_forget()
        self.mensaje.pack_forget()
        self.boton_pausar.pack_forget()
        self.boton_salir.pack_forget()

        self.timer_label.pack(pady=10)
        self.mensaje.pack(pady=2)
        self.boton_pausar.pack(pady=2)
        self.boton_salir.pack(pady=2)

    def mostrar_controles(self):
        self.timer_label.pack_forget()
        self.mensaje.pack_forget()
        self.boton_pausar.pack_forget()
        self.boton_salir.pack_forget()

        self.titulo.pack(pady=4)
        self.label_nombre.pack()
        self.entrada.pack(pady=3)
        self.label_tiempo.pack()
        self.tiempo_entry.pack(pady=3)
        self.label_descanso.pack()
        self.descanso_entry.pack(pady=3)
        self.label_prioridad.pack()
        self.frame_prioridad.pack(pady=3)
        self.boton_agregar.pack(pady=4)
        self.label_seleccionar.pack()
        self.lista.pack(pady=4)
        self.boton_comenzar.pack(pady=3)
        self.boton_pausar.pack(pady=3)
        self.boton_completar.pack(pady=3)
        self.boton_eliminar.pack(pady=3)
        self.label_cronometro.pack(pady=(3))
        self.timer_label.pack(pady=1)
        self.mensaje.pack(pady=1)
        self.boton_salir.pack(pady=1)

    def mostrar_tareas(self):
        self.lista.delete(0, tk.END)

        for tarea in self.pomodoro.tareas:
            estado = "Completada" if tarea["completada"] else "Pendiente"
            texto = f"{tarea['nombre']} | {tarea['tiempo']} min | {tarea['prioridad']} | {estado}"
            self.lista.insert(tk.END, texto)

            ultimo = self.lista.size() - 1

            if tarea["completada"]:
                self.lista.itemconfig(ultimo, fg="gray")
            elif tarea["prioridad"] == "Alta":
                self.lista.itemconfig(ultimo, fg="red")
            elif tarea["prioridad"] == "Media":
                self.lista.itemconfig(ultimo, fg="orange")
            else:
                self.lista.itemconfig(ultimo, fg="green")

    def actualizar_cronometro(self):
        minutos = self.pomodoro.tiempo_restante // 60
        segundos = self.pomodoro.tiempo_restante % 60
        self.timer_label.config(text=f"{minutos:02}:{segundos:02}")

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
        except:
            self.mensaje.config(text="El tiempo debe ser un número entero.")
            return

        nueva_tarea = {
            "nombre": nombre,
            "tiempo": tiempo,
            "prioridad": prioridad,
            "completada": False
        }

        self.pomodoro.tareas.append(nueva_tarea)
        self.mostrar_tareas()

        self.entrada.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)
        self.prioridad_var.set("Media")
        self.mensaje.config(text="")

    def eliminar(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para eliminar.")
            return

        indice = seleccion[0]

        if self.tarea_actual == indice:
            self.detener_temporizador()

        self.pomodoro.tareas.pop(indice)
        self.mostrar_tareas()
        self.mensaje.config(text="")
        
    #BLOQUE 3: TEMPORIZADOR
    def iniciar(self):
        if self.en_cuenta:
            self.mensaje.config(text="El temporizador ya está corriendo.")
            return

        if self.en_descanso:
            self.mensaje.config(text="Ahora mismo estás en descanso.")
            return

        if self.pomodoro.tiempo_restante > 0 and self.tarea_actual is not None:
            self.en_cuenta = True
            self.ocultar_controles()
            nombre = self.pomodoro.tareas[self.tarea_actual]["nombre"]
            self.mensaje.config(text=f"Trabajando en: {nombre}")
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
        self.actualizar_cronometro()
        self.en_cuenta = True
        self.ocultar_controles()
        self.mensaje.config(text=f"Trabajando en: {tarea['nombre']}")
        self.contar()

    def pausar(self):
        if self.en_cuenta:
            self.en_cuenta = False
            self.mostrar_controles()
            self.mensaje.config(text="Temporizador pausado.")
        elif self.en_descanso:
            self.en_descanso = False
            self.mostrar_controles()
            self.mensaje.config(text="Descanso pausado.")
        else:
            self.mensaje.config(text="No hay temporizador en marcha.")

    def completar(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            self.mensaje.config(text="Selecciona una tarea para completar.")
            return

        indice = seleccion[0]
        self.pomodoro.tareas[indice]["completada"] = True
        self.mostrar_tareas()

        if self.tarea_actual == indice:
            self.en_cuenta = False

            if self.trabajo_id is not None:
                try:
                    self.root.after_cancel(self.trabajo_id)
                except:
                    pass
                self.trabajo_id = None

            try:
                descanso = int(self.descanso_entry.get())
                if descanso <= 0:
                    descanso = 5
            except:
                descanso = 5

            self.en_descanso = True
            self.pomodoro.tiempo_restante = descanso * 60
            self.tarea_actual = None
            self.actualizar_cronometro()
            self.ocultar_controles()
            self.mensaje.config(text=f"Descanso: {descanso} minutos")
            self.contar_descanso()
        else:
            self.mensaje.config(text="")

    def detener_temporizador(self):
        self.en_cuenta = False
        self.en_descanso = False
        self.pomodoro.tiempo_restante = 0
        self.tarea_actual = None

        if self.trabajo_id is not None:
            try:
                self.root.after_cancel(self.trabajo_id)
            except:
                pass
            self.trabajo_id = None

        self.timer_label.config(text="00:00")
        self.mostrar_controles()

    def contar(self):
        if self.en_cuenta and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar)

        elif self.pomodoro.tiempo_restante <= 0 and self.en_cuenta:
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.en_cuenta = False
            self.trabajo_id = None
            self.mensaje.config(text="Tiempo terminado. Marca la tarea como completada.")
            self.tarea_actual = None
            self.mostrar_controles()

    def contar_descanso(self):
        if self.en_descanso and self.pomodoro.tiempo_restante > 0:
            self.actualizar_cronometro()
            self.pomodoro.tiempo_restante -= 1
            self.trabajo_id = self.root.after(1000, self.contar_descanso)

        elif self.en_descanso and self.pomodoro.tiempo_restante <= 0:
            self.en_descanso = False
            self.pomodoro.tiempo_restante = 0
            self.actualizar_cronometro()
            self.trabajo_id = None
            self.mostrar_controles()
            self.mensaje.config(text="Descanso terminado. Selecciona la siguiente tarea.")

    def salir(self):
        self.en_cuenta = False
        self.en_descanso = False

        if self.trabajo_id is not None:
            try:
                self.root.after_cancel(self.trabajo_id)
            except:
                pass
            self.trabajo_id = None

        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


app = PomodoroApp()
app.run()
