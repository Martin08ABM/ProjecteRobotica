import tkinter as tk
from tkinter import TOP, messagebox
from datetime import datetime
import os
from turtle import color

# FUNCIONES BÁSICAS PARA CREAR Y ELIMINAR LAS DIFERENTES OPCIONES QUE SE LE DAN AL USUARIO
# FUNCIONES PARA CREAR ELEMENTOS
def crearTarea():
    nombre = entry_nombre_tarea.get().strip()
    descripcion = entrada_descripcion_tarea.get("1.0", tk.END).strip()

    if nombre and descripcion:
        with open("tareas.txt", "a") as archivo_tareas:
            archivo_tareas.write(f"\nTarea: {nombre}\nDescripción: {descripcion}\n\n")
        ruta_archivo = os.path.abspath("tareas.txt")
        messagebox.showinfo("Éxito", f"Tarea '{nombre}' guardada en:\n{ruta_archivo}")
        entry_nombre_tarea.delete(0, tk.END)
        entrada_descripcion_tarea.delete("1.0", tk.END)
    elif not nombre:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea")
    elif not descripcion:
        messagebox.showerror("Error", "Por favor, ingresa la descripción de la tarea")

def crearNotas():
    nombre = entry_nombre_nota.get().strip()
    contenido = entrada_notas.get("1.0", tk.END).strip()

    if nombre and contenido:
        with open("notas.txt", "a") as archivo_notas:
            archivo_notas.write(f"\nNota: {nombre}\nContenido: {contenido}\n\n")
        messagebox.showinfo("Éxito", "Nota guardada correctamente")
        entry_nombre_nota.delete(0, tk.END)
        entrada_notas.delete("1.0", tk.END)
    elif not nombre:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la nota")
    elif not contenido:
        messagebox.showerror("Error", "Por favor, ingresa el contenido de la nota")

def crearRecordatorios():
    nombreRecordatorio = entry_nombre_recordatorio.get().strip()
    fecha = entry_fecha_recordatorio.get().strip()

    if nombreRecordatorio and fecha:
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
            with open("recordatorios.txt", "a") as archivo_recordatorios:
                archivo_recordatorios.write(f"\nRecordatorio: {nombreRecordatorio}\nFecha: {fecha}\n\n")
            messagebox.showinfo("Éxito", f"Recordatorio '{nombreRecordatorio}' guardado para el día: {fecha}")
            entry_nombre_recordatorio.delete(0, tk.END)
            entry_fecha_recordatorio.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "La fecha no es correcta, usa dd/mm/yyyy")
    elif not nombreRecordatorio:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del recordatorio")
    elif not fecha:
        messagebox.showerror("Error", "Por favor, ingresa la fecha del recordatorio")

# FUNCIONES PARA ELIMINAR ELEMENTOS
def eliminarTarea():
    nombre_tarea_eliminar = entry_eliminar_tarea.get().strip()

    if not nombre_tarea_eliminar:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea a eliminar")
        return

    try:
        with open("tareas.txt", "r") as archivo:
            lineas = archivo.readlines()

        nueva_lista = []
        tarea_encontrada = False
        i = 0

        while i < len(lineas):
            if lineas[i].strip().startswith(f"Tarea: {nombre_tarea_eliminar}"):
                tarea_encontrada = True
                i += 3
            else:
                nueva_lista.append(lineas[i])
                i += 1

        if not tarea_encontrada:
            messagebox.showinfo("Información", f"No se encontró '{nombre_tarea_eliminar}'")
            return

        with open("tareas.txt", "w") as archivo:
            archivo.writelines(nueva_lista)

        messagebox.showinfo("Éxito", f"Tarea '{nombre_tarea_eliminar}' eliminada")
        entry_eliminar_tarea.delete(0, tk.END)

    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de tareas no encontrado")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def eliminarNota():
    nombreNotaEliminar = entry_eliminar_nota.get().strip()

    if nombreNotaEliminar:
        try:
            with open("notas.txt", "r") as archivo_notas:
                lineas = archivo_notas.readlines()
            with open("notas.txt", "w") as archivo_notas:
                nota_encontrada = False
                for i in range(0, len(lineas), 2):
                    if nombreNotaEliminar not in lineas[i]:
                        archivo_notas.writelines(lineas[i:i+2])
                    else:
                        nota_encontrada = True
                if nota_encontrada:
                    messagebox.showinfo("Éxito", f"Nota eliminada.")
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombreNotaEliminar}'.")
            entry_eliminar_nota.delete(0, tk.END)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de notas no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showerror("Error", "Ingresa el nombre de la nota a eliminar")

def eliminarRecordatorio():
    nombre_recordatorio_eliminar = entry_eliminar_recordatorio.get().strip()

    if nombre_recordatorio_eliminar:
        try:
            with open("recordatorios.txt", "r") as archivo_recordatorios:
                lineas = archivo_recordatorios.readlines()

            with open("recordatorios.txt", "w") as archivo_recordatorios:
                recordatorio_encontrado = False
                for i in range(0, len(lineas), 3):
                    if nombre_recordatorio_eliminar not in lineas[i]:
                        archivo_recordatorios.writelines(lineas[i:i+3])
                    else:
                        recordatorio_encontrado = True
                if recordatorio_encontrado:
                    messagebox.showinfo("Éxito", f"Recordatorio eliminado.")
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombre_recordatorio_eliminar}'.")
            entry_eliminar_recordatorio.delete(0, tk.END)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de recordatorios no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showerror("Error", "Ingresa el nombre del recordatorio a eliminar")

# LÓGICA PARA QUE SE IMPRIMA UNA VENTANA EN PANTALLA CON LA QUE EL USUARIO PUEDA INTERACTUAR
# Apartado de creación de la pantalla principal, con la que el usuario interactuará (contiene estilos globales, título, tamaño, etc.)
pantalla = tk.Tk()
pantalla.configure(background="#F0F4F8")
pantalla.title("Notas, Recordatorios y Tareas")
pantalla.geometry("450x460")

# Frame para la creación de elementos
frame_crear = tk.Frame(pantalla)
frame_crear.grid(row=1, column=0, columnspan=3)

# Texto "Qué quieres hacer"
label_que_hacer = tk.Label(pantalla, text="¿Qué quieres hacer?", font=("Arial", 10, "bold"), foreground="#2C3E50")
label_que_hacer.grid(row=0, column=0, columnspan=1, sticky="nsew", pady=10, padx=15)
label_que_hacer.configure(background="#F0F4F8")

# Frame para los botones de selección horizontal
frame_botones_seleccion = tk.Frame(pantalla)
frame_botones_seleccion.grid(row=5, column=3, columnspan=1)

# ELEMENTOS DE LA PARTE GRÁFICA
# FUNCIONES PARA AÑADIR LOS DIFERENTES ELEMENTOS
# Función para añadir un elemento (tarea, nota, recordatorio)
def añadirTarea():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Tarea
    label_nombre_tarea = tk.Label(frame_crear, text="Nombre de la tarea:", width=15)
    label_nombre_tarea.configure(background="#34495E")
    label_nombre_tarea.grid()
    global entry_nombre_tarea
    entry_nombre_tarea = tk.Entry(frame_crear)
    entry_nombre_tarea.grid()

    label_descripcion_tarea = tk.Label(frame_crear, text="Descripción de la tarea:")
    label_descripcion_tarea.grid()
    global entrada_descripcion_tarea
    entrada_descripcion_tarea = tk.Text(frame_crear, width=30, height=15)
    entrada_descripcion_tarea.grid()

    global boton_crear_tarea
    boton_crear_tarea = tk.Button(frame_crear, text="Crear tarea", command=crearTarea, width=40)
    boton_crear_tarea.configure(background="#2980B9", pady=10, padx=10)
    boton_crear_tarea.grid()

def añadirNota():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Nota
    label_nombre_nota = tk.Label(frame_crear, text="Nombre de la nota:", width=40)
    label_nombre_nota.grid()
    global entry_nombre_nota
    entry_nombre_nota = tk.Entry(frame_crear)
    entry_nombre_nota.grid()

    label_contenido_nota = tk.Label(frame_crear, text="Contenido de la nota:")
    label_contenido_nota.grid()
    global entrada_notas
    entrada_notas = tk.Text(frame_crear, height=5, width=30)
    entrada_notas.grid()

    global boton_crear_nota
    boton_crear_nota = tk.Button(frame_crear, text="Crear nota", command=crearNotas, width=40)
    boton_crear_nota.configure(background="#2980B9")
    boton_crear_nota.grid()

def añadirRecordatorio():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Recordatorio
    label_nombre_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio:", width=40)
    label_nombre_recordatorio.grid()
    global entry_nombre_recordatorio
    entry_nombre_recordatorio = tk.Entry(frame_crear)
    entry_nombre_recordatorio.grid()

    label_fecha_recordatorio = tk.Label(frame_crear, text="Fecha (dd/mm/yyyy):")
    label_fecha_recordatorio.grid()
    global entry_fecha_recordatorio
    entry_fecha_recordatorio = tk.Entry(frame_crear)
    entry_fecha_recordatorio.grid()

    global boton_crear_recordatorio
    boton_crear_recordatorio = tk.Button(frame_crear, text="Crear recordatorio", command=crearRecordatorios, width=30)
    boton_crear_recordatorio.configure(background="#2980B9")

    boton_crear_recordatorio.grid()

# FUNCIONES PARA ELIMINAR ELEMENTOS
def eliminarTareaInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_tarea = tk.Label(frame_crear, text="Nombre de la tarea a eliminar:", width=40)
    label_eliminar_tarea.grid()
    global entry_eliminar_tarea
    entry_eliminar_tarea = tk.Entry(frame_crear)
    entry_eliminar_tarea.grid()

    boton_eliminar_tarea = tk.Button(frame_crear, text="Eliminar tarea", command=eliminarTarea, width=40)
    boton_eliminar_tarea.configure(background="#2980B9")
    boton_eliminar_tarea.grid()

def eliminarNotaInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_nota = tk.Label(frame_crear, text="Nombre de la nota a eliminar:", width=40)
    label_eliminar_nota.grid()
    global entry_eliminar_nota
    entry_eliminar_nota = tk.Entry(frame_crear)
    entry_eliminar_nota.grid()

    boton_eliminar_nota = tk.Button(frame_crear, text="Eliminar nota", command=eliminarNota, width=40)
    boton_eliminar_nota.configure(background="#2980B9")
    boton_eliminar_nota.grid()

def eliminarRecordatorioInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio a eliminar:", width=40)
    label_eliminar_recordatorio.grid()
    global entry_eliminar_recordatorio
    entry_eliminar_recordatorio = tk.Entry(frame_crear)
    entry_eliminar_recordatorio.grid()

    boton_eliminar_recordatorio = tk.Button(frame_crear, text="Eliminar recordatorio", command=eliminarRecordatorio)
    boton_eliminar_recordatorio.configure(background="#2980B9")
    boton_eliminar_recordatorio.grid()

# BOTONES DE SELECCIÓN DE LAS ACCIONES
# Botones elección de añadir un elemento
boton_seleccion_tarea = tk.Button(pantalla, text="Añadir tarea", takefocus=False, command=añadirTarea)
boton_seleccion_tarea.grid(row=2, column=0, padx=10, pady=10)

boton_seleccion_nota = tk.Button(pantalla, text="Añadir nota", takefocus=False, command=añadirNota)
boton_seleccion_nota.grid(row=2, column=1, padx=10, pady=10)

boton_seleccion_recordatorio = tk.Button(pantalla, text="Añadir recordatorio", takefocus=False, command=añadirRecordatorio)
boton_seleccion_recordatorio.grid(row=2, column=2, padx=10, pady=10)

# Frame para la eliminación de elementos
frame_eliminar = tk.Frame(pantalla)
frame_eliminar.grid()

# Botones elección de eliminar un elemento
boton_eliminar_tarea_interfaz = tk.Button(pantalla, text="Eliminar tarea", takefocus=False, command=eliminarTareaInterfaz)
boton_eliminar_tarea_interfaz.grid(row=3, column=0, padx=10, pady=10)

boton_eliminar_nota_interfaz = tk.Button(pantalla, text="Eliminar nota", takefocus=False, command=eliminarNotaInterfaz)
boton_eliminar_nota_interfaz.grid(row=3, column=1, padx=10, pady=10)

boton_eliminar_recordatorio_interfaz = tk.Button(pantalla, text="Eliminar recordatorio", takefocus=False, command=eliminarRecordatorioInterfaz)
boton_eliminar_recordatorio_interfaz.grid(row=3, column=2, padx=10, pady=10)

# Bucle para que se muestre el programa
pantalla.mainloop()
