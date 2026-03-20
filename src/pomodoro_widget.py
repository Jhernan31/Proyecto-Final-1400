import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -----------------------------
# Variables globales
# -----------------------------
tareas = []
temporizador_activo = False
tiempo_restante = 0
tarea_actual = None

# -----------------------------
# Agregar tarea
# -----------------------------
def agregar_tarea():
    nombre = entrada_tarea.get()
    prioridad = prioridad_var.get()

    # Condicional 1 y 2
    if nombre == "":
        messagebox.showerror("Error", "Ingrese una tarea")
        return

    if prioridad not in ["Alta", "Media", "Baja"]:
        messagebox.showerror("Error", "Prioridad no válida")
        return

    tarea = {"nombre": nombre, "prioridad": prioridad, "completada": False}
    tareas.append(tarea)

    lista_tareas.insert(tk.END, nombre)

    # Colores
    if prioridad == "Alta":
        lista_tareas.itemconfig(tk.END, {'fg': 'red'})
    elif prioridad == "Media":
        lista_tareas.itemconfig(tk.END, {'fg': 'orange'})
    else:
        lista_tareas.itemconfig(tk.END, {'fg': 'green'})

    entrada_tarea.delete(0, tk.END)

# -----------------------------
# Iniciar temporizador
# -----------------------------
def iniciar_temporizador():
    global tiempo_restante, temporizador_activo, tarea_actual

    seleccion = lista_tareas.curselection()

    if not seleccion:
        messagebox.showerror("Error", "Seleccione una tarea")
        return

    try:
        minutos = int(entrada_tiempo.get())
        if minutos <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Tiempo inválido")
        return

    tarea_actual = tareas[seleccion[0]]
    tiempo_restante = minutos * 60
    temporizador_activo = True

    cuenta_regresiva()

# -----------------------------
# Cuenta regresiva
# -----------------------------
def cuenta_regresiva():
    global tiempo_restante, temporizador_activo

    if tiempo_restante > 0 and temporizador_activo:
        mins = tiempo_restante // 60
        secs = tiempo_restante % 60

        etiqueta_timer.config(text=f"{mins:02}:{secs:02}")

        tiempo_restante -= 1
        ventana.after(1000, cuenta_regresiva)

    elif tiempo_restante == 0:
        etiqueta_timer.config(text="¡Tiempo terminado!")
        mensaje_final()

# -----------------------------
# Pausar
# -----------------------------
def pausar_temporizador():
    global temporizador_activo

    if temporizador_activo:
        temporizador_activo = False
        messagebox.showinfo("Info", "Temporizador pausado")
    else:
        messagebox.showwarning("Info", "No hay temporizador activo")

# -----------------------------
# Reiniciar
# -----------------------------
def reiniciar_temporizador():
    global tiempo_restante, temporizador_activo

    tiempo_restante = 0
    temporizador_activo = False
    etiqueta_timer.config(text="00:00")

# -----------------------------
# Completar tarea
# -----------------------------
def completar_tarea():
    seleccion = lista_tareas.curselection()

    if not seleccion:
        messagebox.showerror("Error", "Seleccione una tarea")
        return

    indice = seleccion[0]
    tareas[indice]["completada"] = True

    lista_tareas.itemconfig(indice, {'bg': 'lightgray'})

    messagebox.showinfo("Éxito", "Tarea completada")

# -----------------------------
# Eliminar tarea
# -----------------------------
def eliminar_tarea():
    seleccion = lista_tareas.curselection()

    if not seleccion:
        messagebox.showerror("Error", "Seleccione una tarea")
        return

    indice = seleccion[0]

    lista_tareas.delete(indice)
    tareas.pop(indice)

# -----------------------------
# Mensaje final
# -----------------------------
def mensaje_final():
    messagebox.showinfo(
        "Pomodoro",
        "¡Tiempo terminado!\nExcelente trabajo.\nTe has ganado una recompensa 🎉"
    )

# -----------------------------
# Reloj
# -----------------------------
def actualizar_reloj():
    ahora = datetime.now()
    etiqueta_reloj.config(text=ahora.strftime("%d/%m/%Y %H:%M:%S"))
    ventana.after(1000, actualizar_reloj)

# -----------------------------
# Interfaz
# -----------------------------
ventana = tk.Tk()
ventana.title("Widget Pomodoro")
ventana.geometry("400x550")
ventana.attributes("-topmost", True)

# Reloj
etiqueta_reloj = tk.Label(ventana, font=("Arial", 10))
etiqueta_reloj.pack()

# Entrada tarea
tk.Label(ventana, text="Nueva tarea").pack()
entrada_tarea = tk.Entry(ventana)
entrada_tarea.pack()

# Prioridad
tk.Label(ventana, text="Prioridad").pack()
prioridad_var = tk.StringVar(value="Media")

tk.Radiobutton(ventana, text="Alta", variable=prioridad_var, value="Alta").pack()
tk.Radiobutton(ventana, text="Media", variable=prioridad_var, value="Media").pack()
tk.Radiobutton(ventana, text="Baja", variable=prioridad_var, value="Baja").pack()

# Botón agregar
tk.Button(ventana, text="Agregar tarea", command=agregar_tarea).pack()

# Lista tareas
tk.Label(ventana, text="Lista de tareas").pack()
lista_tareas = tk.Listbox(ventana, width=40, height=8)
lista_tareas.pack()

# Tiempo
tk.Label(ventana, text="Minutos").pack()
entrada_tiempo = tk.Entry(ventana)
entrada_tiempo.pack()

# Botones control
tk.Button(ventana, text="Iniciar", command=iniciar_temporizador).pack(pady=5)
tk.Button(ventana, text="Pausar", command=pausar_temporizador).pack(pady=5)
tk.Button(ventana, text="Reiniciar", command=reiniciar_temporizador).pack(pady=5)

# Tareas
tk.Button(ventana, text="Completar tarea", command=completar_tarea).pack(pady=5)
tk.Button(ventana, text="Eliminar tarea", command=eliminar_tarea).pack(pady=5)

# Timer
etiqueta_timer = tk.Label(ventana, text="00:00", font=("Arial", 24))
etiqueta_timer.pack()

# Salir
tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=10)

# Iniciar reloj
actualizar_reloj()

ventana.mainloop()
