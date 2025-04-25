# Importaciones generales
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from datetime import datetime, timedelta
import os
from notifypy import Notify

# FUNCIONES BÁSICAS PARA CREAR Y ELIMINAR LAS DIFERENTES OPCIONES QUE SE LE DAN AL USUARIO
# FUNCIONES PARA CREAR ELEMENTOS Y GUARDARLOS (BACKEND)

#Función para crear tareas y guardarlas
def crearTarea():
    # Variables propias de la función
    nombre = entry_nombre_tarea.get().strip()
    descripcion = entrada_descripcion_tarea.get("1.0", tk.END).strip()

    # Lógica de guardado
    if nombre and descripcion:
        with open("tareas.txt", "a") as archivo_tareas:
            archivo_tareas.write(f"\nTarea: {nombre}\nDescripción: {descripcion}\n\n")
        messagebox.showinfo("Éxito", f"Tarea '{nombre}' guardada") # Mensaje de  éxito en caso de que el guardado de la tarea sea correcto
        entry_nombre_tarea.delete(0, tk.END)
        entrada_descripcion_tarea.delete("1.0", tk.END)
        actualizar_visualizaciones()  # Actualizar visualización después de crear una tarea
    elif not nombre:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea") # Mensaje de error en caso de faltar el nombre de la tarea
    elif not descripcion:
        messagebox.showerror("Error", "Por favor, ingresa la descripción de la tarea") # Mensaje de error en caso de faltar el contenido de la tarea

# Funcion para crear notas y guardarlas
def crearNotas():
    # Variables propias de la función
    nombre = entry_nombre_nota.get().strip()
    contenido = entrada_notas.get("1.0", tk.END).strip()

    # Lógica de guardado
    if nombre and contenido:
        with open("notas.txt", "a") as archivo_notas:
            archivo_notas.write(f"\nNota: {nombre}\nContenido: {contenido}\n\n")
        messagebox.showinfo("Éxito", "Nota guardada correctamente") # Mensaje de  éxito en caso de que el guardado de la nota sea correcta
        entry_nombre_nota.delete(0, tk.END)
        entrada_notas.delete("1.0", tk.END)
        actualizar_visualizaciones()  # Actualizar visualización después de crear una nota
    elif not nombre:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la nota") # Mensaje de error en caso de faltar el nombre de la nota
    elif not contenido:
        messagebox.showerror("Error", "Por favor, ingresa el contenido de la nota") # Mensaje de error en caso de faltar el contenido de la nota

# Función para crear recordatorios y guardarlos
def crearRecordatorios():
    # Variables propias
    nombreRecordatorio = entry_nombre_recordatorio.get().strip()
    fecha_str = entry_fecha_recordatorio.get().strip()

    # Lógica de guardado
    if nombreRecordatorio and fecha_str:
        try:
            fechaRecordatorio = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            with open("recordatorios.txt", "a") as archivo_recordatorios:
                archivo_recordatorios.write(f"\nRecordatorio: {nombreRecordatorio}\nFecha: {fechaRecordatorio}\n\n")
            messagebox.showinfo("Éxito", f"Recordatorio '{nombreRecordatorio}' guardado para el día: {fechaRecordatorio}") # Mensaje de  éxito en caso de que el guardado de la tarea sea correcto
            entry_nombre_recordatorio.delete(0, tk.END)
            entry_fecha_recordatorio.delete(0, tk.END)
            actualizar_visualizaciones()  # Actualizar visualización después de crear un recordatorio

            # Programar la notificación
            programarNotificacion(nombreRecordatorio, fechaRecordatorio)

        except ValueError:
            messagebox.showerror("Error", "La fecha no es correcta, usa dd/mm/yyyy") # Mensaje de error en caso de que la fecha no tenga el formato correcto
    elif not nombreRecordatorio:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del recordatorio") # Mensaje de error en case de que falte el nombre el nombre del recordatorio
    elif not fecha_str:
        messagebox.showerror("Error", "Por favor, ingresa la fecha del recordatorio") # Mensaje de error en caso de faltar el contenido del recordatorio

def programarNotificacion(nombreRecordatorio, fechaRecordatorio):
    diaDeHoy = date.today()
    if fechaRecordatorio == diaDeHoy:
        ahora = datetime.now()
        # Programar para 20 segundos después de la hora actual
        horaNotificacion = ahora + timedelta(seconds=10)
        diferencia = (horaNotificacion - ahora).total_seconds()
        pantalla.after(int(diferencia * 1000), enviar_notificacion, nombreRecordatorio)
    elif fechaRecordatorio > diaDeHoy:
        # Programar para el día del recordatorio a las 00:00:20
        fecha_hora_notificacion = datetime(fechaRecordatorio.year, fechaRecordatorio.month, fechaRecordatorio.day, 0, 0, 20)
        ahora = datetime.now()
        if fecha_hora_notificacion > ahora:
            diferencia = (fecha_hora_notificacion - ahora).total_seconds()
            pantalla.after(int(diferencia * 1000), enviar_notificacion, nombreRecordatorio)

def enviar_notificacion(nombreRecordatorio):
    notification = Notify()
    notification.title = f"{nombreRecordatorio}"
    notification.message = f"El recordatorio {nombreRecordatorio} ha llegado"
    notification.send()


# FUNCIONES PARA ELIMINAR ELEMENTOS (BACKEND)

#Función para eliminar una tarea
def eliminarTarea():
    # Variables propias
    nombre_tarea_eliminar = entry_eliminar_tarea.get().strip()

    if not nombre_tarea_eliminar:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea a eliminar") # Mensaje de error en caso de no encontrar la tarea con el nombre especificado
        return

    # Si se encuentra la tarea, se usa esta lógica para eliminar la tarea
    try:
        with open("tareas.txt", "r") as archivo:
            lineas = archivo.readlines()

        nueva_lista = []
        tarea_encontrada = False
        i = 0

        while i < len(lineas):
            if lineas[i].strip().startswith(f"Tarea: {nombre_tarea_eliminar}"): # Mensaje de éxito si se ha eliminado correctamente la tarea
                tarea_encontrada = True
                i += 3
            else:
                nueva_lista.append(lineas[i])
                i += 1

        if not tarea_encontrada:
            messagebox.showinfo("Información", f"No se encontró '{nombre_tarea_eliminar}'") # Mensaje de error en caso de que la tarea no se encuentre
            return

        with open("tareas.txt", "w") as archivo:
            archivo.writelines(nueva_lista)

        messagebox.showinfo("Éxito", f"Tarea '{nombre_tarea_eliminar}' eliminada") # Mensaje de éxito cuándo se haya elominado la tarea
        entry_eliminar_tarea.delete(0, tk.END)
        actualizar_visualizaciones()  # Actualizar visualización después de eliminar una tarea

    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de tareas no encontrado") # Mensaje de error en caso de que el archivo en el que se guarden las tareas no se encuentre
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}") # Mensaje de error en casi de algún error extraño

# Función para eliminar las notas
def eliminarNota():
    # Variables propias
    nombreNotaEliminar = entry_eliminar_nota.get().strip()

    # Lógica para eliminar la nota
    if nombreNotaEliminar:
        try:
            with open("notas.txt", "r") as archivo_notas:
                lineas = archivo_notas.readlines()
            with open("notas.txt", "w") as archivo_notas:
                nota_encontrada = False
                i = 0
                while i < len(lineas):
                    if not lineas[i].strip().startswith(f"Nota: {nombreNotaEliminar}"): # Guardar la nota
                        archivo_notas.write(lineas[i])
                    else:
                        nota_encontrada = True
                        # Saltar la línea de la nota y su contenido
                        i += 1
                        if i < len(lineas) and lineas[i].strip().startswith("Contenido:"): # Contenido de la nota que se guarda en el documento
                            i += 1
                            # Saltar línea vacía si existe
                            if i < len(lineas) and lineas[i].strip() == "":
                                i += 1
                                continue
                    i += 1

                if nota_encontrada:
                    messagebox.showinfo("Éxito", f"Nota '{nombreNotaEliminar}' eliminada.") # Mensaje de éxito en caso de que se haya eliminado correctamente la nota
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombreNotaEliminar}'.") # Mensaje de error en caso de que no se haya encontrado la nota
            entry_eliminar_nota.delete(0, tk.END)
            actualizar_visualizaciones()  # Actualizar visualización después de eliminar una nota
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de notas no encontrado") # Mensaje de error en caso de que no se haya encontrado el archivo de guardado de las notas
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") # Mensaje de error
    else:
        messagebox.showerror("Error", "Ingresa el nombre de la nota a eliminar") # Mensaje de error en caso de que no se haya introducido el nombre de la nota en el campo especificado

# Función para eliminar recordatorios
def eliminarRecordatorio():
    # Variables propias
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
                    messagebox.showinfo("Éxito", f"Recordatorio '{nombre_recordatorio_eliminar}' eliminado.") # Mensaje de éxito cuando se elimina el recordatorio
                else:
                    messagebox.showerror("Error", f"No se encontró '{nombre_recordatorio_eliminar}'.") # Mensaje de error si no se encuentra el recordatorio
            entry_eliminar_recordatorio.delete(0, tk.END)
            actualizar_visualizaciones()  # Actualizar visualización después de eliminar un recordatorio
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de recordatorios no encontrado") # Mensaje de error si no se encuentra el archivo de recordatorios
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}") # Mensaje de error general
    else:
        messagebox.showerror("Error", "Ingresa el nombre del recordatorio a eliminar") # Mensaje de error si no se ingresa el nombre del recordatorio

# LÓGICA PARA QUE SE IMPRIMA UNA VENTANA EN PANTALLA CON LA QUE EL USUARIO PUEDA INTERACTUAR
# Apartado de creación de la pantalla principal, con la que el usuario interactuará (contiene estilos globales, título, tamaño, etc.)
pantalla = tk.Tk()
pantalla.configure(background="#F0F3F4") # Color de fondo de la app
pantalla.title("Notas, Recordatorios y Tareas") # Nombre de la app
pantalla.geometry("800x675")  # Tamaño inicial más grande para acomodar la visualización

# Configurar los pesos de filas y columnas para responsividad
pantalla.grid_columnconfigure(0, weight=1)
pantalla.grid_columnconfigure(1, weight=1)
pantalla.grid_columnconfigure(2, weight=1)
for i in range(10):  # Configurar 10 filas para ser flexibles
    pantalla.grid_rowconfigure(i, weight=1)

# Pantalla para la creación de elementos con configuración responsive
frame_crear = tk.Frame(pantalla, bg="#F0F4F8")
frame_crear.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_crear.grid_columnconfigure(0, weight=1)

# Título "Qué quieres hacer"
label_que_hacer = tk.Label(pantalla, text="¿Qué quieres hacer?", font=("Arial", 12, "bold"), foreground="#2C3E50", bg="#F0F4F8")
label_que_hacer.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10, padx=15)

# Pantalla para visualización de elementos guardados
frame_visualizacion = tk.Frame(pantalla, bg="#ECF0F1", bd=2, relief=tk.GROOVE)
frame_visualizacion.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_visualizacion.grid_columnconfigure(0, weight=1)
frame_visualizacion.grid_rowconfigure(0, weight=0)  # El título no crece
frame_visualizacion.grid_rowconfigure(1, weight=1)  # El notebook crece

# Título del pantalla de visualización
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
                    text_tareas.insert(tk.END, "No hay tareas guardadas.") # Mensaje si no hay tareas guardadas
        else:
            text_tareas.insert(tk.END, "No hay tareas guardadas.") # Mensaje si el archivo no existe
    except Exception as e:
        text_tareas.insert(tk.END, f"Error al cargar tareas: {e}") # Mensaje de error al cargar
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
                    text_notas.insert(tk.END, "No hay notas guardadas.") # Mensaje si no hay notas guardadas
        else:
            text_notas.insert(tk.END, "No hay notas guardadas.") # Mensaje si el archivo no existe
    except Exception as e:
        text_notas.insert(tk.END, f"Error al cargar notas: {e}") # Mensaje de error al cargar
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
                    text_recordatorios.insert(tk.END, "No hay recordatorios guardados.") # Mensaje si no hay recordatorios guardados
        else:
            text_recordatorios.insert(tk.END, "No hay recordatorios guardados.") # Mensaje si el archivo no existe
    except Exception as e:
        text_recordatorios.insert(tk.END, f"Error al cargar recordatorios: {e}") # Mensaje de error al cargar
    text_recordatorios.config(state=tk.DISABLED)

# Función para actualizar la subpantalla de visualización de las cosas ya guardadas (tareas, notas o recordatorios)
def actualizar_visualizaciones():
    cargar_tareas()
    cargar_notas()
    cargar_recordatorios()


# FUNCIONES PARA AÑADIR LOS DIFERENTES ELEMENTOS (FRONTEND)
# FUNCIONES PARA CREAR LOS ELEMENTOS Y GUARDARLOS (FRONTEND)

# Función para añadir una tarea, parte gráfica
def añadirTarea():
    # Limpiar pantalla
        widget.destroy()

    # Lógica con la que aparecen inputs al usuario para que rellene los campos de infromación requerida
    label_nombre_tarea = tk.Label(frame_crear, text="Nombre de la tarea:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_tarea.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    global entry_nombre_tarea
    entry_nombre_tarea = tk.Entry(frame_crear) # Renderizado de la caja donde se agrega el nombre de la tarea
    entry_nombre_tarea.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_descripcion_tarea = tk.Label(frame_crear, text="Descripción de la tarea:", bg="#34495E", fg="white", padx=5, pady=5)
    label_descripcion_tarea.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Renderizado de la caja en la que escribirá el usuario

    global entrada_descripcion_tarea
    entrada_descripcion_tarea = tk.Text(frame_crear, width=30, height=5)
    entrada_descripcion_tarea.grid(row=3, column=0, sticky="nsew", padx=5, pady=5) # Zona para añadir la descripción de la tarea

    global boton_crear_tarea
    boton_crear_tarea = tk.Button(frame_crear, text="Crear tarea", command=crearTarea, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_tarea.grid(row=4, column=0, sticky="ew", padx=5, pady=5) # Botón para guardar la tarea

# Función para añadir una nota, parte gráfica
def añadirNota():
    # Limpiar pantalla
    for widget in frame_crear.winfo_children():
        widget.destroy()

    # Lógica con la que aparecen los inputs necesarios para que el usuario rellene los campos necesarios con la información requerida
    label_nombre_nota = tk.Label(frame_crear, text="Nombre de la nota:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_nota.grid(row=0, column=0, sticky="ew", padx=5, pady=5) # Renderizado de la caja donde se agrega el nombre de la nota

    global entry_nombre_nota
    entry_nombre_nota = tk.Entry(frame_crear)
    entry_nombre_nota.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_contenido_nota = tk.Label(frame_crear, text="Contenido de la nota:", bg="#34495E", fg="white", padx=5, pady=5)
    label_contenido_nota.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Renderizado de la caja en la que el usuario escribirá el contenido de la nota

    global entrada_notas
    entrada_notas = tk.Text(frame_crear, height=5, width=30)
    entrada_notas.grid(row=3, column=0, sticky="nsew", padx=5, pady=5) # Zona para añadir la descripción de la nota

    global boton_crear_nota
    boton_crear_nota = tk.Button(frame_crear, text="Crear nota", command=crearNotas, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_nota.grid(row=4, column=0, sticky="ew", padx=5, pady=5) # Botón para guardar la nota

def añadirRecordatorio():
    # Limpiar pantalla
    for widget in frame_crear.winfo_children():
        widget.destroy()

# Lógica con la que aparecen los inputs necesarios para que el usuario rellene los campos necesarios con la informació solicitada
    label_nombre_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio:", bg="#34495E", fg="white", padx=5, pady=5)
    label_nombre_recordatorio.grid(row=0, column=0, sticky="ew", padx=5, pady=5) # Renderizado de la caja donde se agrega el nombre del recordatorio

    global entry_nombre_recordatorio
    entry_nombre_recordatorio = tk.Entry(frame_crear)
    entry_nombre_recordatorio.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    label_fecha_recordatorio = tk.Label(frame_crear, text="Fecha (dd/mm/yyyy):", bg="#34495E", fg="white", padx=5, pady=5)
    label_fecha_recordatorio.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Renderizado de la caja en la que el usuario escribirá la fecha en la que quiere que le salga el recordatorio

    global entry_fecha_recordatorio
    entry_fecha_recordatorio = tk.Entry(frame_crear)
    entry_fecha_recordatorio.grid(row=3, column=0, sticky="ew", padx=5, pady=5) # Zona para añadir la descripción de la nota

    global boton_crear_recordatorio
    boton_crear_recordatorio = tk.Button(frame_crear, text="Crear recordatorio", command=crearRecordatorios, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_crear_recordatorio.grid(row=4, column=0, sticky="ew", padx=5, pady=5) # Botón para guardar la nota

# FUNCIONES PARA ELIMINAR ELEMENTOS (FRONTEND)

# Función para eliminar tareas (sección del frontend)
def eliminarTareaInterfaz():
    # Limpiar pantalla
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_tarea = tk.Label(frame_crear, text="Nombre de la tarea a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_tarea.grid(row=0, column=0, sticky="ew", padx=5, pady=5) # Renderizado del apartado en el que se pide al usuario el nombre de la tarea que desea eliminar

    global entry_eliminar_tarea
    entry_eliminar_tarea = tk.Entry(frame_crear)
    entry_eliminar_tarea.grid(row=1, column=0, sticky="ew", padx=5, pady=5) # Entrada del nombre de la tarea que se quiere eliminar

    boton_eliminar_tarea = tk.Button(frame_crear, text="Eliminar tarea", command=eliminarTarea, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_tarea.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Botón para eliminar la tarea

# Función para eliminar notas (sección del frontend)
def eliminarNotaInterfaz():
    # Limpiar pantalla
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_nota = tk.Label(frame_crear, text="Nombre de la nota a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_nota.grid(row=0, column=0, sticky="ew", padx=5, pady=5) # Renderizado del apartado en el que se le pide al usuario el nombre de la nota que desea eliminar

    global entry_eliminar_nota
    entry_eliminar_nota = tk.Entry(frame_crear)
    entry_eliminar_nota.grid(row=1, column=0, sticky="ew", padx=5, pady=5) # Entrada del nombre de la nota que se quiere eliminar

    boton_eliminar_nota = tk.Button(frame_crear, text="Eliminar nota", command=eliminarNota, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_nota.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Botón para eliminar la nota

# Función para eliminar los recordatorios (sección del frontend)
def eliminarRecordatorioInterfaz():
    # Limpiar pantalla
    for widget in frame_crear.winfo_children():
        widget.destroy()

    label_eliminar_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio a eliminar:", bg="#34495E", fg="white", padx=5, pady=5)
    label_eliminar_recordatorio.grid(row=0, column=0, sticky="ew", padx=5, pady=5) # Renderizado del apartado en el que se le pide al usuario el nombre del recordatorio que desea eliminar

    global entry_eliminar_recordatorio
    entry_eliminar_recordatorio = tk.Entry(frame_crear)
    entry_eliminar_recordatorio.grid(row=1, column=0, sticky="ew", padx=5, pady=5) # Entrada del nombre del recordatorio que se quiere eliminar

    boton_eliminar_recordatorio = tk.Button(frame_crear, text="Eliminar recordatorio", command=eliminarRecordatorio, bg="#2980B9", fg="white", padx=10, pady=10)
    boton_eliminar_recordatorio.grid(row=2, column=0, sticky="ew", padx=5, pady=5) # Botón para eliminar el recordatorio

# Reglas principales de la pantalla para los botones de acciones
frame_botones = tk.Frame(pantalla, bg="#F0F3F4") # Color de fondo de los botones
frame_botones.grid(row=2, column=0, columnspan=3, sticky="ew") # Posición de los botones en la pantalla
frame_botones.grid_columnconfigure(0, weight=1) # Primera columna de botones
frame_botones.grid_columnconfigure(1, weight=1) # Segunda columna de botonea
frame_botones.grid_columnconfigure(2, weight=1) # Tercera columna de botones

# BOTONES DE SELECCIÓN DE LAS ACCIONES (Grid)

# BOTONES PARA ALADIR UN ELEMENTO

# Botón de selección de la acción de añadir una tarea
boton_seleccion_tarea = tk.Button(pantalla, text="Añadir tarea", command=añadirTarea, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_tarea.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Botón de selección de la acción de añadir una nota
boton_seleccion_nota = tk.Button(pantalla, text="Añadir nota", command=añadirNota, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_nota.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Botón de selección de la acción de añadir un recordatorio
boton_seleccion_recordatorio = tk.Button(pantalla, text="Añadir recordatorio", command=añadirRecordatorio, bg="#3498DB", fg="white", padx=10, pady=5)
boton_seleccion_recordatorio.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

# BOTONES PARA ELIMINAR UN ELEMENTO

# Botón de selección de la acción de eliminar una tarea
boton_eliminar_tarea_interfaz = tk.Button(pantalla, text="Eliminar tarea", command=eliminarTareaInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_tarea_interfaz.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

# Botón de selección de la acción de eliminar una nota
boton_eliminar_nota_interfaz = tk.Button(pantalla, text="Eliminar nota", command=eliminarNotaInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_nota_interfaz.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Botón de selección de la acción de eliminar un recordatorio
boton_eliminar_recordatorio_interfaz = tk.Button(pantalla, text="Eliminar recordatorio", command=eliminarRecordatorioInterfaz, bg="#E74C3C", fg="white", padx=10, pady=5)
boton_eliminar_recordatorio_interfaz.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

# FUNCIÓN PARA MANEJAR EL EVENTO DE REDIMENSIÓN DE LA VENTANA PRINCIPAL
def on_window_resize(event):
    # Obtener el nuevo tamaño de la ventana
    width = event.width
    height = event.height

    # Ajustar los tamaños de los widgets según sea necesario
    if width < 600:  # Tamaño pequeño en caso de que la ventana sea pequeña
        for text_widget in [text_tareas, text_notas, text_recordatorios]:
            text_widget.config(width=30, height=5)
    else:  # En caso que la ventana sea grande, ajustar el tamaño de la ventana a grande
        for text_widget in [text_tareas, text_notas, text_recordatorios]:
            text_widget.config(width=0, height=10)

# VINCULAR EL EVENTO PREVIO PARA QUE SE EJECUTE CON LA FUNCIÓN "configure"
pantalla.bind("<Configure>", on_window_resize) #

# CARGAR LOS DATOS PREVIAMENTE GUARDADOS EN LOS ARCHIVOS CORRESPONDIENTES
actualizar_visualizaciones()

# BUCLE PRINCIPAL PARA QUE SE MUESTRE EL PROGRAMA
# Y SE RENDERIZE EN LA PANTALLA
pantalla.mainloop()

# Proyecto de robótica hecho por Martin Adolfo alumno de 1ro de Bachillerato