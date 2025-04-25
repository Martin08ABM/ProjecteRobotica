import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

# FUNCIONES BÁSICAS PARA CREAR Y ELIMINAR LAS DIFERENTES OPCIONES QUE SE LE DAN AL USUARIO
# FUNCIONES PARA CREAR ELEMENTOS
def crearTarea():
    nombre = entry_nombre_tarea.get().strip()
    descripcion = entrada_descripcion_tarea.get("1.0", tk.END).strip()

    if nombre and descripcion:
        with open("tareas.txt", "a") as archivo_tareas:
            archivo_tareas.write(f"\nTarea: {nombre}\nDescripción: {descripcion}\n\n")
        messagebox.showinfo("Éxito", f"Tarea '{nombre}' guardada")
        entry_nombre_tarea.delete(0, tk.END)
        entrada_descripcion_tarea.delete("1.0", tk.END)
        actualizar_visualizaciones()  # Actualizar visualización después de crear una tarea
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
        actualizar_visualizaciones()  # Actualizar visualización después de crear una nota
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
            actualizar_visualizaciones()  # Actualizar visualización después de crear un recordatorio
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
        actualizar_visualizaciones()  # Actualizar visualización después de eliminar una tarea

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
                i = 0
                while i < len(lineas):
                    if not lineas[i].strip().startswith(f"Nota: {nombreNotaEliminar}"):
                        archivo_notas.write(lineas[i])
                    else:
                        nota_encontrada = True
                        # Saltar la línea de la nota y su contenido
                        i += 1
                        if i < len(lineas) and lineas[i].strip().startswith("Contenido:"):
                            i += 1
                            # Saltar línea vacía si existe
                            if i < len(lineas) and lineas[i].strip() == "":
                                i += 1
                            continue
                    i += 1
                
                if nota_encontrada:
                    messagebox.showinfo("Éxito", f"Nota '{nombreNotaEliminar}' eliminada.")
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombreNotaEliminar}'.")
            entry_eliminar_nota.delete(0, tk.END)
            actualizar_visualizaciones()  # Actualizar visualización después de eliminar una nota
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
                i = 0
                while i < len(lineas):
                    if not lineas[i].strip().startswith(f"Recordatorio: {nombre_recordatorio_eliminar}"):
                        archivo_recordatorios.write(lineas[i])
                    else:
                        recordatorio_encontrado = True
                        # Saltar la línea del recordatorio y su fecha
                        i += 1
                        if i < len(lineas) and lineas[i].strip().startswith("Fecha:"):
                            i += 1
                            # Saltar línea vacía si existe
                            if i < len(lineas) and lineas[i].strip() == "":
                                i += 1
                            continue
                    i += 1
                
                if recordatorio_encontrado:
                    messagebox.showinfo("Éxito", f"Recordatorio '{nombre_recordatorio_eliminar}' eliminado.")
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombre_recordatorio_eliminar}'.")
            entry_eliminar_recordatorio.delete(0, tk.END)
            actualizar_visualizaciones()  # Actualizar visualización después de eliminar un recordatorio
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de recordatorios no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    else:
        messagebox.showerror("Error", "Ingresa el nombre del recordatorio a eliminar")

# LÓGICA PARA QUE SE IMPRIMA UNA VENTANA EN PANTALLA CON LA QUE EL USUARIO PUEDA INTERACTUAR
# Apartado de creación de la pantalla principal, con la que el usuario interactuará (contiene estilos globales, título, tamaño, etc.)
pantalla = tk.Tk()
pantalla.configure(background="#F0F3F4")
pantalla.title("Notas, Recordatorios y Tareas")
pantalla.geometry("800x600")  # Tamaño inicial más grande para acomodar la visualización

# Configurar los pesos de filas y columnas para responsividad
pantalla.grid_columnconfigure(0, weight=1)
pantalla.grid_columnconfigure(1, weight=1)
pantalla.grid_columnconfigure(2, weight=1)
for i in range(10):  # Configurar 10 filas para ser flexibles
    pantalla.grid_rowconfigure(i, weight=1)

# Frame para la creación de elementos con configuración responsive
frame_crear = tk.Frame(pantalla, bg="#F0F4F8")
frame_crear.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_crear.grid_columnconfigure(0, weight=1)

# Texto "Qué quieres hacer"
label_que_hacer = tk.Label(pantalla, text="¿Qué quieres hacer?", font=("Arial", 10, "bold"), foreground="#2C3E50", bg="#F0F4F8")
label_que_hacer.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10, padx=15)

# Frame para visualización de elementos guardados
frame_visualizacion = tk.Frame(pantalla, bg="#ECF0F1", bd=2, relief=tk.GROOVE)
frame_visualizacion.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_visualizacion.grid_columnconfigure(0, weight=1)
frame_visualizacion.grid_rowconfigure(0, weight=0)  # La fila del título no crece
frame_visualizacion.grid_rowconfigure(1, weight=1)  # La fila del notebook crece

# Título del frame de visualización
label_visualizacion = tk.Label(frame_visualizacion, text="Elementos Guardados", font=("Arial", 10, "bold"), bg="#ECF0F1")
label_visualizacion.grid(row=0, column=0, sticky="ew", pady=5)

# Notebook para mostrar tareas, notas y recordatorios en pestañas
notebook = ttk.Notebook(frame_visualizacion)
notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

# Pestañas para el notebook
tab_tareas = tk.Frame(notebook, bg="#FFFFFF")
tab_notas = tk.Frame(notebook, bg="#FFFFFF")
tab_recordatorios = tk.Frame(notebook, bg="#FFFFFF")

# Configurar responsividad de las pestañas
for tab in [tab_tareas, tab_notas, tab_recordatorios]:
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_rowconfigure(0, weight=1)

# Añadir pestañas al notebook
notebook.add(tab_tareas, text="Tareas")
notebook.add(tab_notas, text="Notas")
notebook.add(tab_recordatorios, text="Recordatorios")

# TextWidgets para mostrar el contenido
text_tareas = tk.Text(tab_tareas, wrap=tk.WORD, width=50, height=10, bg="#F0F3F4")
text_tareas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
scrollbar_tareas = tk.Scrollbar(tab_tareas, command=text_tareas.yview)
scrollbar_tareas.grid(row=0, column=1, sticky="ns")
text_tareas.config(yscrollcommand=scrollbar_tareas.set)

text_notas = tk.Text(tab_notas, wrap=tk.WORD, width=50, height=10, bg="#F0F3F4")
text_notas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
scrollbar_notas = tk.Scrollbar(tab_notas, command=text_notas.yview)
scrollbar_notas.grid(row=0, column=1, sticky="ns")
text_notas.config(yscrollcommand=scrollbar_notas.set)

text_recordatorios = tk.Text(tab_recordatorios, wrap=tk.WORD, width=50, height=10, bg="#F0F3F4")
text_recordatorios.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
scrollbar_recordatorios = tk.Scrollbar(tab_recordatorios, command=text_recordatorios.yview)
scrollbar_recordatorios.grid(row=0, column=1, sticky="ns")
text_recordatorios.config(yscrollcommand=scrollbar_recordatorios.set)

# Botón para actualizar visualización
boton_actualizar = tk.Button(frame_visualizacion, text="Actualizar Visualización", command=lambda: actualizar_visualizaciones(), bg="#3498DB", fg="white")
boton_actualizar.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# ELEMENTOS DE LA PARTE GRÁFICA
# FUNCIONES PARA VISUALIZAR LOS ELEMENTOS GUARDADOS
def cargar_tareas():
    text_tareas.config(state=tk.NORMAL)
    text_tareas.delete(1.0, tk.END)
    try:
        if os.path.exists("tareas.txt"):
            with open("tareas.txt", "r") as archivo:
                contenido = archivo.read()
                if contenido.strip():
                    text_tareas.insert(tk.END, contenido)
                else:
                    text_tareas.insert(tk.END, "No hay tareas guardadas.")
        else:
            text_tareas.insert(tk.END, "No hay tareas guardadas.")
    except Exception as e:
        text_tareas.insert(tk.END, f"Error al cargar tareas: {e}")
    text_tareas.config(state=tk.DISABLED)

def cargar_notas():
    text_notas.config(state=tk.NORMAL)
    text_notas.delete(1.0, tk.END)
    try:
        if os.path.exists("notas.txt"):
            with open("notas.txt", "r") as archivo:
                contenido = archivo.read()
                if contenido.strip():
                    text_notas.insert(tk.END, contenido)
                else:
                    text_notas.insert(tk.END, "No hay notas guardadas.")
        else:
            text_notas.insert(tk.END, "No hay notas guardadas.")
    except Exception as e:
        text_notas.insert(tk.END, f"Error al cargar notas: {e}")
    text_notas.config(state=tk.DISABLED)

def cargar_recordatorios():
    text_recordatorios.config(state=tk.NORMAL)
    text_recordatorios.delete(1.0, tk.END)
    try:
        if os.path.exists("recordatorios.txt"):
            with open("recordatorios.txt", "r") as archivo:
                contenido = archivo.read()
                if contenido.strip():
                    text_recordatorios.insert(tk.END, contenido)
                else:
                    text_recordatorios.insert(tk.END, "No hay recordatorios guardados.")
        else:
            text_recordatorios.insert(tk.END, "No hay recordatorios guardados.")
    except Exception as e:
        text_recordatorios.insert(tk.END, f"Error al cargar recordatorios: {e}")
    text_recordatorios.config(state=tk.DISABLED)

def actualizar_visualizaciones():
    cargar_tareas()
    cargar_notas()
    cargar_recordatorios()

# FUNCIONES PARA AÑADIR LOS DIFERENTES ELEMENTOS
# Función para añadir un elemento (tarea, nota, recordatorio)
def añadirTarea():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Tarea
    label_nombre_tarea = tk.Label(frame_crear, text="Nombre de la tarea:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_tarea.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_nombre_tarea
    entry_nombre_tarea = tk.Entry(frame_crear)
    entry_nombre_tarea.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_descripcion_tarea = tk.Label(frame_crear, text="Descripción de la tarea:", bg="#34495E", fg="white", padx=5, pady=5)
    label_descripcion_tarea.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    
    global entrada_descripcion_tarea
    entrada_descripcion_tarea = tk.Text(frame_crear, width=30, height=5)
    entrada_descripcion_tarea.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

    global boton_crear_tarea
    boton_crear_tarea = tk.Button(frame_crear, text="Crear tarea", command=crearTarea, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_tarea.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

def añadirNota():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Nota
    label_nombre_nota = tk.Label(frame_crear, text="Nombre de la nota:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_nota.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_nombre_nota
    entry_nombre_nota = tk.Entry(frame_crear)
    entry_nombre_nota.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_contenido_nota = tk.Label(frame_crear, text="Contenido de la nota:", bg="#34495E", fg="white", padx=5, pady=5)
    label_contenido_nota.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    
    global entrada_notas
    entrada_notas = tk.Text(frame_crear, height=5, width=30)
    entrada_notas.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

    global boton_crear_nota
    boton_crear_nota = tk.Button(frame_crear, text="Crear nota", command=crearNotas, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_nota.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

def añadirRecordatorio():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Recordatorio
    label_nombre_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_recordatorio.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_nombre_recordatorio
    entry_nombre_recordatorio = tk.Entry(frame_crear)
    entry_nombre_recordatorio.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_fecha_recordatorio = tk.Label(frame_crear, text="Fecha (dd/mm/yyyy):", bg="#34495E", fg="white", padx=5, pady=5)
    label_fecha_recordatorio.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_fecha_recordatorio
    entry_fecha_recordatorio = tk.Entry(frame_crear)
    entry_fecha_recordatorio.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

    global boton_crear_recordatorio
    boton_crear_recordatorio = tk.Button(frame_crear, text="Crear recordatorio", command=crearRecordatorios, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_recordatorio.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

# FUNCIONES PARA ELIMINAR ELEMENTOS
def eliminarTareaInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_tarea = tk.Label(frame_crear, text="Nombre de la tarea a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_tarea.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_eliminar_tarea
    entry_eliminar_tarea = tk.Entry(frame_crear)
    entry_eliminar_tarea.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    boton_eliminar_tarea = tk.Button(frame_crear, text="Eliminar tarea", command=eliminarTarea, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_tarea.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

def eliminarNotaInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_nota = tk.Label(frame_crear, text="Nombre de la nota a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_nota.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_eliminar_nota
    entry_eliminar_nota = tk.Entry(frame_crear)
    entry_eliminar_nota.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    boton_eliminar_nota = tk.Button(frame_crear, text="Eliminar nota", command=eliminarNota, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_nota.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

def eliminarRecordatorioInterfaz():
    # Limpiar frame
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_recordatorio.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    global entry_eliminar_recordatorio
    entry_eliminar_recordatorio = tk.Entry(frame_crear)
    entry_eliminar_recordatorio.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    boton_eliminar_recordatorio = tk.Button(frame_crear, text="Eliminar recordatorio", command=eliminarRecordatorio, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_recordatorio.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

# Frame para los botones de acciones
frame_botones = tk.Frame(pantalla, bg="#F0F3F4")
frame_botones.grid(row=2, column=0, columnspan=3, sticky="ew")
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)
frame_botones.grid_columnconfigure(2, weight=1)

# BOTONES DE SELECCIÓN DE LAS ACCIONES
# Botones elección de añadir un elemento
boton_seleccion_tarea = tk.Button(pantalla, text="Añadir tarea", command=añadirTarea, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_tarea.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

boton_seleccion_nota = tk.Button(pantalla, text="Añadir nota", command=añadirNota, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_nota.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

boton_seleccion_recordatorio = tk.Button(pantalla, text="Añadir recordatorio", command=añadirRecordatorio, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_recordatorio.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

# Botones elección de eliminar un elemento
boton_eliminar_tarea_interfaz = tk.Button(pantalla, text="Eliminar tarea", command=eliminarTareaInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_tarea_interfaz.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

boton_eliminar_nota_interfaz = tk.Button(pantalla, text="Eliminar nota", command=eliminarNotaInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_nota_interfaz.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

boton_eliminar_recordatorio_interfaz = tk.Button(pantalla, text="Eliminar recordatorio", command=eliminarRecordatorioInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_recordatorio_interfaz.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

# Función para manejar el evento de cambio de tamaño de la ventana
def on_window_resize(event):
    # Obtener el nuevo tamaño de la ventana
    width = event.width
    height = event.height
    
    # Ajustar tamaños de widgets según sea necesario
    if width < 600:  # Ventana pequeña
        for text_widget in [text_tareas, text_notas, text_recordatorios]:
            text_widget.config(width=30, height=5)
    else:  # Ventana grande
        for text_widget in [text_tareas, text_notas, text_recordatorios]:
            text_widget.config(width=0, height=10)

# Vincular función al evento de cambio de tamaño
pantalla.bind("<Configure>", on_window_resize)

# Cargar datos iniciales
actualizar_visualizaciones()

# Bucle para que se muestre el programa
pantalla.mainloop()
