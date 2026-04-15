import tkinter as tk
from tkinter import messagebox
import json
import os


# ============================================================
# BLOQUE 1: CLASE PRINCIPAL
# Esta clase crea la ventana principal y controla toda la lógica
# del widget Pomodoro.
# ============================================================
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # Ajuste de escalado para evitar que Windows agrande
        # demasiado letras y controles.
        # ----------------------------------------------------
        self.tk.call("tk", "scaling", 1.0)

        # ----------------------------------------------------
        # Configuración de la ventana principal
        # ----------------------------------------------------
        self.title("Widget Pomodoro")
        self.geometry("380x640")
        self.resizable(False, False)

        # ----------------------------------------------------
        # Archivo JSON donde se guardan las tareas
        # ----------------------------------------------------
        self.archivo = "tareas.json"

        # ----------------------------------------------------
        # Lista donde se almacenan las tareas
        # ----------------------------------------------------
        self.tareas = []

        # ----------------------------------------------------
        # Variables del temporizador
        # ----------------------------------------------------
        self.tiempo_restante = 0
        self.descanso_restante = 0
        self.temporizador_activo = False
        self.en_descanso = False
        self.after_id = None
        self.indice_actual = None

        # ----------------------------------------------------
        # Variable para guardar la prioridad seleccionada
        # ----------------------------------------------------
        self.prioridad_var = tk.StringVar(value="Media")

        # ----------------------------------------------------
        # Cargar tareas guardadas y construir interfaz
        # ----------------------------------------------------
        self.cargar_tareas()
        self.crear_widgets()
        self.actualizar_lista()

    # ========================================================
    # BLOQUE 2: CREACIÓN DE LA INTERFAZ
    # Aquí se crean etiquetas, entradas, botones y lista.
    # ========================================================
    def crear_widgets(self):
        self.titulo = tk.Label(self, text="Widget Pomodoro", font=("Arial", 15, "bold"))
        self.titulo.pack(pady=10)

        self.label_nombre = tk.Label(self, text="Tarea", font=("Arial", 10))
        self.label_nombre.pack()
        self.entrada = tk.Entry(self, font=("Arial", 10), width=26)
        self.entrada.pack(pady=3)

        self.label_tiempo = tk.Label(self, text="Minutos de trabajo", font=("Arial", 10))
        self.label_tiempo.pack(pady=(6, 0))
        self.tiempo_entry = tk.Entry(self, font=("Arial", 10), width=8)
        self.tiempo_entry.pack(pady=3)

        self.label_descanso = tk.Label(self, text="Minutos de descanso", font=("Arial", 10))
        self.label_descanso.pack(pady=(6, 0))
        self.descanso_entry = tk.Entry(self, font=("Arial", 10), width=8)
        self.descanso_entry.pack(pady=3)
        self.descanso_entry.insert(0, "5")

        self.label_prioridad = tk.Label(self, text="Prioridad", font=("Arial", 10))
        self.label_prioridad.pack(pady=(8, 3))

        self.frame_prioridad = tk.Frame(self)
        self.frame_prioridad.pack()

        self.radio_alta = tk.Radiobutton(
            self.frame_prioridad,
            text="Alta",
            variable=self.prioridad_var,
            value="Alta",
            font=("Arial", 9)
        )
        self.radio_alta.pack(side="left", padx=6)

        self.radio_media = tk.Radiobutton(
            self.frame_prioridad,
            text="Media",
            variable=self.prioridad_var,
            value="Media",
            font=("Arial", 9)
        )
        self.radio_media.pack(side="left", padx=6)

        self.radio_baja = tk.Radiobutton(
            self.frame_prioridad,
            text="Baja",
            variable=self.prioridad_var,
            value="Baja",
            font=("Arial", 9)
        )
        self.radio_baja.pack(side="left", padx=6)

        # Lista visual de tareas
        self.lista = tk.Listbox(
            self,
            width=34,
            height=7,
            font=("Arial", 9),
            exportselection=False
        )
        self.lista.pack(pady=10)

        # Marco de botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(pady=6)

        self.boton_agregar = tk.Button(
            self.frame_botones,
            text="Agregar",
            width=12,
            font=("Arial", 9),
            command=self.agregar_tarea
        )
        self.boton_agregar.grid(row=0, column=0, padx=4, pady=3)

        self.boton_comenzar = tk.Button(
            self.frame_botones,
            text="Comenzar",
            width=12,
            font=("Arial", 9),
            command=self.comenzar_temporizador
        )
        self.boton_comenzar.grid(row=0, column=1, padx=4, pady=3)

        self.boton_pausar = tk.Button(
            self.frame_botones,
            text="Pausar",
            width=12,
            font=("Arial", 9),
            command=self.pausar_temporizador
        )
        self.boton_pausar.grid(row=1, column=0, padx=4, pady=3)

        self.boton_completar = tk.Button(
            self.frame_botones,
            text="Completar",
            width=12,
            font=("Arial", 9),
            command=self.completar_tarea
        )
        self.boton_completar.grid(row=1, column=1, padx=4, pady=3)

        self.boton_eliminar = tk.Button(
            self.frame_botones,
            text="Eliminar",
            width=12,
            font=("Arial", 9),
            command=self.eliminar_tarea
        )
        self.boton_eliminar.grid(row=2, column=0, padx=4, pady=3)

        self.boton_reiniciar = tk.Button(
            self.frame_botones,
            text="Reiniciar tarea",
            width=12,
            font=("Arial", 9),
            command=self.reiniciar_tarea
        )
        self.boton_reiniciar.grid(row=2, column=1, padx=4, pady=3)

        self.boton_continuar = tk.Button(
            self.frame_botones,
            text="Continuar",
            width=12,
            font=("Arial", 9),
            command=self.continuar_temporizador
        )
        self.boton_continuar.grid(row=3, column=0, padx=4, pady=3)

        self.timer_label = tk.Label(self, text="00:00", font=("Arial", 18, "bold"))
        self.timer_label.pack(pady=(10, 5))

        self.mensaje = tk.Label(self, text="", font=("Arial", 9), wraplength=320)
        self.mensaje.pack(pady=3)

        self.recompensa_label = tk.Label(
            self,
            text="",
            font=("Arial", 9, "bold"),
            fg="blue",
            wraplength=320,
            justify="center"
        )
        self.recompensa_label.pack(pady=4)

        self.boton_salir = tk.Button(
            self,
            text="Salir",
            width=12,
            font=("Arial", 9),
            command=self.destroy
        )
        self.boton_salir.pack(pady=8)

    # ========================================================
    # BLOQUE 3: CARGAR TAREAS DESDE JSON
    # ========================================================
    def cargar_tareas(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as archivo:
                    self.tareas = json.load(archivo)
            except Exception:
                self.tareas = []
        else:
            self.tareas = []

    # ========================================================
    # BLOQUE 4: GUARDAR TAREAS EN JSON
    # ========================================================
    def guardar_tareas(self):
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(self.tareas, archivo, indent=4, ensure_ascii=False)

    # ========================================================
    # BLOQUE 5: COLOR POR PRIORIDAD
    # ========================================================
    def color_prioridad(self, prioridad):
        if prioridad == "Alta":
            return "red"
        elif prioridad == "Media":
            return "orange"
        else:
            return "green"

    # ========================================================
    # BLOQUE 6: ACTUALIZAR LISTA VISUAL
    # ========================================================
    def actualizar_lista(self):
        self.lista.delete(0, tk.END)

        for i, tarea in enumerate(self.tareas):
            texto = f'{tarea["nombre"]} - {tarea["tiempo"]} min - {tarea["prioridad"]}'

            if tarea["completada"]:
                texto += " - ✔"

            self.lista.insert(tk.END, texto)
            self.lista.itemconfig(i, fg=self.color_prioridad(tarea["prioridad"]))

    # ========================================================
    # BLOQUE 7: AGREGAR TAREA
    # ========================================================
    def agregar_tarea(self):
        nombre = self.entrada.get().strip()
        tiempo = self.tiempo_entry.get().strip()
        descanso = self.descanso_entry.get().strip()
        prioridad = self.prioridad_var.get()

        if not nombre:
            messagebox.showerror("Error", "Debes escribir una tarea.")
            return

        if not tiempo.isdigit() or int(tiempo) <= 0:
            messagebox.showerror("Error", "El tiempo de trabajo debe ser un número mayor que 0.")
            return

        if not descanso.isdigit() or int(descanso) <= 0:
            messagebox.showerror("Error", "El tiempo de descanso debe ser un número mayor que 0.")
            return

        nueva_tarea = {
            "nombre": nombre,
            "tiempo": int(tiempo),
            "descanso": int(descanso),
            "prioridad": prioridad,
            "completada": False
        }

        self.tareas.append(nueva_tarea)
        self.guardar_tareas()
        self.actualizar_lista()

        self.entrada.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)
        self.descanso_entry.delete(0, tk.END)
        self.descanso_entry.insert(0, "5")
        self.prioridad_var.set("Media")

        self.mensaje.config(text="Tarea agregada.")
        self.recompensa_label.config(text="")

    # ========================================================
    # BLOQUE 8: COMENZAR TEMPORIZADOR
    # Inicia desde cero la tarea seleccionada.
    # ========================================================
    def comenzar_temporizador(self):
        if self.temporizador_activo:
            return

        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea para comenzar.")
            return

        indice = seleccion[0]
        tarea = self.tareas[indice]

        if tarea["completada"]:
            messagebox.showinfo("Aviso", "Esa tarea ya está completada.")
            return

        self.indice_actual = indice

        # Si no está en descanso, reinicia el tiempo de trabajo
        if not self.en_descanso:
            self.tiempo_restante = tarea["tiempo"] * 60

        # Si estaba en descanso pero no hay tiempo guardado, lo vuelve a cargar
        if self.en_descanso and self.descanso_restante <= 0:
            self.descanso_restante = tarea["descanso"] * 60

        self.temporizador_activo = True
        self.actualizar_temporizador()

    # ========================================================
    # BLOQUE 9: CONTINUAR TEMPORIZADOR
    # Reanuda desde donde fue pausado.
    # ========================================================
    def continuar_temporizador(self):
        if self.temporizador_activo:
            return

        if self.tiempo_restante <= 0 and self.descanso_restante <= 0:
            messagebox.showwarning("Aviso", "No hay temporizador para continuar.")
            return

        self.temporizador_activo = True

        if self.en_descanso:
            self.mensaje.config(text="Reanudando descanso...")
        else:
            self.mensaje.config(text="Reanudando trabajo...")

        self.actualizar_temporizador()

    # ========================================================
    # BLOQUE 10: ACTUALIZAR TEMPORIZADOR
    # ========================================================
    def actualizar_temporizador(self):
        if not self.temporizador_activo:
            return

        if self.en_descanso:
            minutos = self.descanso_restante // 60
            segundos = self.descanso_restante % 60
            self.timer_label.config(text=f"{minutos:02}:{segundos:02}")
            self.mensaje.config(text="Tiempo de descanso.")

            if self.descanso_restante > 0:
                self.descanso_restante -= 1
                self.after_id = self.after(1000, self.actualizar_temporizador)
            else:
                self.en_descanso = False
                self.temporizador_activo = False
                self.after_id = None
                self.timer_label.config(text="00:00")
                self.mensaje.config(text="Descanso terminado.")
        else:
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            self.timer_label.config(text=f"{minutos:02}:{segundos:02}")
            self.mensaje.config(text="Trabajando en la tarea...")

            if self.tiempo_restante > 0:
                self.tiempo_restante -= 1
                self.after_id = self.after(1000, self.actualizar_temporizador)
            else:
                self.temporizador_activo = False
                self.after_id = None
                self.timer_label.config(text="00:00")
                self.mensaje.config(text="Tiempo de trabajo terminado. Ahora descansa.")
                self.iniciar_descanso()

    # ========================================================
    # BLOQUE 11: INICIAR DESCANSO
    # ========================================================
    def iniciar_descanso(self):
        if self.indice_actual is None:
            return

        tarea = self.tareas[self.indice_actual]
        self.descanso_restante = tarea["descanso"] * 60
        self.en_descanso = True
        self.temporizador_activo = True
        self.actualizar_temporizador()

    # ========================================================
    # BLOQUE 12: PAUSAR TEMPORIZADOR
    # ========================================================
    def pausar_temporizador(self):
        self.temporizador_activo = False

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.mensaje.config(text="Temporizador pausado.")

    # ========================================================
    # BLOQUE 13: COMPLETAR TAREA
    # ========================================================
    def completar_tarea(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea para completar.")
            return

        indice = seleccion[0]
        self.tareas[indice]["completada"] = True
        self.guardar_tareas()
        self.actualizar_lista()

        self.temporizador_activo = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.tiempo_restante = 0
        self.descanso_restante = 0
        self.en_descanso = False
        self.indice_actual = None

        self.timer_label.config(text="00:00")
        self.mensaje.config(text="Tarea completada.")

        if self.todas_completadas():
            self.recompensa_label.config(
                text="¡Felicitaciones! Has cumplido con todas tus tareas. Te has ganado una recompensa."
            )
        else:
            self.recompensa_label.config(text="")

    # ========================================================
    # BLOQUE 14: ELIMINAR TAREA
    # ========================================================
    def eliminar_tarea(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar.")
            return

        indice = seleccion[0]
        del self.tareas[indice]

        self.guardar_tareas()
        self.actualizar_lista()

        self.temporizador_activo = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.tiempo_restante = 0
        self.descanso_restante = 0
        self.en_descanso = False
        self.indice_actual = None

        self.timer_label.config(text="00:00")
        self.mensaje.config(text="Tarea eliminada.")
        self.recompensa_label.config(text="")

    # ========================================================
    # BLOQUE 15: REINICIAR SOLO UNA TAREA
    # ========================================================
    def reiniciar_tarea(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una tarea para reiniciar.")
            return

        indice = seleccion[0]

        if self.indice_actual == indice:
            self.temporizador_activo = False

            if self.after_id:
                self.after_cancel(self.after_id)
                self.after_id = None

            self.tiempo_restante = 0
            self.descanso_restante = 0
            self.en_descanso = False
            self.indice_actual = None
            self.timer_label.config(text="00:00")

        self.tareas[indice]["completada"] = False

        self.guardar_tareas()
        self.actualizar_lista()

        self.mensaje.config(text="La tarea seleccionada fue reiniciada.")
        self.recompensa_label.config(text="")

    # ========================================================
    # BLOQUE 16: VERIFICAR SI TODAS LAS TAREAS ESTÁN COMPLETAS
    # ========================================================
    def todas_completadas(self):
        if not self.tareas:
            return False
        return all(tarea["completada"] for tarea in self.tareas)


# ============================================================
# BLOQUE 17: PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
