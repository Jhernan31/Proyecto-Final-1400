import tkinter as tk
from tkinter import messagebox
import json
import os


# BLOQUE 1: DEFINICIÓN DE LA CLASE PRINCIPAL


class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Widget Pomodoro")
        self.geometry("500x800")
        self.resizable(False, False)

        # Archivo donde se guardarán las tareas
        self.archivo = "tareas.json"

        # Lista que almacena todas las tareas
        self.tareas = []

        # VARIABLES DEL TEMPORIZADOR
        
        self.tiempo_restante = 0
        self.descanso_restante = 0
        self.temporizador_activo = False
        self.en_descanso = False
        self.after_id = None
        self.indice_actual = None

        # Variable para guardar la prioridad seleccionada
        self.prioridad_var = tk.StringVar(value="Media")

        # Cargar tareas desde archivo JSON
        self.cargar_tareas()

        # Crear interfaz gráfica
        self.crear_widgets()

        # Mostrar tareas en pantalla
        self.actualizar_lista()



# BLOQUE 2: CREACIÓN DE LA INTERFAZ GRÁFICA


    def crear_widgets(self):

        # Título principal
        self.titulo = tk.Label(self, text="Widget Pomodoro", font=("Arial", 22, "bold"))
        self.titulo.pack(pady=20)

        # Entrada de nombre de tarea
        self.label_nombre = tk.Label(self, text="Tarea")
        self.label_nombre.pack()
        self.entrada = tk.Entry(self)
        self.entrada.pack()

        # Entrada de tiempo de trabajo
        self.label_tiempo = tk.Label(self, text="Minutos de trabajo")
        self.label_tiempo.pack()
        self.tiempo_entry = tk.Entry(self)
        self.tiempo_entry.pack()

        # Entrada de tiempo de descanso
        self.label_descanso = tk.Label(self, text="Minutos de descanso")
        self.label_descanso.pack()
        self.descanso_entry = tk.Entry(self)
        self.descanso_entry.pack()
        self.descanso_entry.insert(0, "5")

        # Selección de prioridad
        self.prioridad_var = tk.StringVar(value="Media")

        tk.Radiobutton(self, text="Alta", variable=self.prioridad_var, value="Alta").pack()
        tk.Radiobutton(self, text="Media", variable=self.prioridad_var, value="Media").pack()
        tk.Radiobutton(self, text="Baja", variable=self.prioridad_var, value="Baja").pack()

        # Lista donde se muestran las tareas
        self.lista = tk.Listbox(self, width=40)
        self.lista.pack(pady=10)

        # Botones principales
        tk.Button(self, text="Agregar", command=self.agregar_tarea).pack()
        tk.Button(self, text="Comenzar", command=self.comenzar_temporizador).pack()
        tk.Button(self, text="Pausar", command=self.pausar_temporizador).pack()
        tk.Button(self, text="Completar", command=self.completar_tarea).pack()
        tk.Button(self, text="Eliminar", command=self.eliminar_tarea).pack()
        tk.Button(self, text="Reiniciar tareas", command=self.reiniciar_tareas).pack()

        # Etiqueta del temporizador
        self.timer_label = tk.Label(self, text="00:00", font=("Arial", 24))
        self.timer_label.pack()

        # Mensajes
        self.mensaje = tk.Label(self, text="")
        self.mensaje.pack()

        self.recompensa_label = tk.Label(self, text="", fg="blue")
        self.recompensa_label.pack()


# BLOQUE 3: MANEJO DE ARCHIVOS (JSON)


    def cargar_tareas(self):
        # Carga las tareas desde el archivo JSON si existe
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.tareas = json.load(f)

    def guardar_tareas(self):
        # Guarda las tareas en el archivo JSON
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, indent=4)


# BLOQUE 4: ACTUALIZACIÓN DE LA LISTA VISUAL


    def actualizar_lista(self):
        # Limpia la lista
        self.lista.delete(0, tk.END)

        # Vuelve a insertar todas las tareas
        for tarea in self.tareas:
            texto = f'{tarea["nombre"]} - {tarea["tiempo"]} min - {tarea["prioridad"]}'

            # Si la tarea está completada, añade ✔
            if tarea["completada"]:
                texto += " ✔"

            self.lista.insert(tk.END, texto)

# BLOQUE 5: FUNCIONES PRINCIPALES


    def agregar_tarea(self):
        # Obtiene datos del usuario
        nombre = self.entrada.get()
        tiempo = self.tiempo_entry.get()
        descanso = self.descanso_entry.get()

        # Validaciones básicas
        if not nombre or not tiempo.isdigit():
            messagebox.showerror("Error", "Datos inválidos")
            return

        # Crear nueva tarea
        tarea = {
            "nombre": nombre,
            "tiempo": int(tiempo),
            "descanso": int(descanso),
            "prioridad": self.prioridad_var.get(),
            "completada": False
        }

        # Guardar tarea
        self.tareas.append(tarea)
        self.guardar_tareas()
        self.actualizar_lista()


# BLOQUE 6: TEMPORIZADOR


    def comenzar_temporizador(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        self.indice_actual = seleccion[0]
        tarea = self.tareas[self.indice_actual]

        self.tiempo_restante = tarea["tiempo"] * 60
        self.temporizador_activo = True

        self.actualizar_temporizador()

    def actualizar_temporizador(self):
        # Controla el conteo regresivo
        if not self.temporizador_activo:
            return

        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60

        self.timer_label.config(text=f"{minutos:02}:{segundos:02}")

        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1

            # after ejecuta esta función cada 1 segundo
            self.after_id = self.after(1000, self.actualizar_temporizador)
        else:
            self.temporizador_activo = False
            self.mensaje.config(text="Tiempo terminado")


# BLOQUE 7: CONTROL DEL TEMPORIZADOR


    def pausar_temporizador(self):
        # Detiene el temporizador
        self.temporizador_activo = False

        if self.after_id:
            self.after_cancel(self.after_id)


# BLOQUE 8: ACCIONES SOBRE TAREAS


    def completar_tarea(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        self.tareas[seleccion[0]]["completada"] = True
        self.guardar_tareas()
        self.actualizar_lista()

        # Verifica si todas están completas
        if all(t["completada"] for t in self.tareas):
            self.recompensa_label.config(
                text="¡Felicitaciones! Has completado todas las tareas"
            )

    def eliminar_tarea(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        del self.tareas[seleccion[0]]
        self.guardar_tareas()
        self.actualizar_lista()


# BLOQUE 9: REINICIAR TAREAS (EL ERROR QUE TENÍAS)


    def reiniciar_tareas(self):

        # Detener temporizador
        self.temporizador_activo = False

        if self.after_id:
            self.after_cancel(self.after_id)

        # Resetear estado de todas las tareas
        for tarea in self.tareas:
            tarea["completada"] = False

        # Resetear variables
        self.tiempo_restante = 0
        self.en_descanso = False
        self.indice_actual = None

        # Actualizar interfaz
        self.timer_label.config(text="00:00")
        self.mensaje.config(text="Tareas reiniciadas")
        self.recompensa_label.config(text="")

        self.guardar_tareas()
        self.actualizar_lista()


# BLOQUE 10: EJECUCIÓN DEL PROGRAMA


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
