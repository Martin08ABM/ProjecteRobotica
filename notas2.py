# Importaciones generales
from cProfile import label
from datetime import datetime
from tkinter import * 
from tkinter import messagebox
import tkinter as tk

# FUNCIONES BÁSICAS PARA CREAR Y ELIMINAR LAS DIFERENTES OPCIONES QUE SE LE DAN AL USUARIO
# Función para crear tareas
def crearTarea():
    nombre = entry_nombre_tarea.get() # Nombre de la tarea
    descripcion = entrada_descripcion_tarea.get("1.0", END).strip() # Descripción de la tarea
        
    # Validar si los campos están rellenos o no y guardar en caso positivo
    if nombre and descripcion:
        with open("tareas.txt", "a") as archivo_tareas:
            archivo_tareas.write(f"\nTarea: {nombre}\nDescripción: {descripcion}\n\n")
        messagebox.showinfo("Éxito", f"La tarea `{nombre}` se a guardado correctamente, la puedes revisar y/o editar en") #Completar más tarde !!IMPORTANTE
    elif nombre and not descripcion:
        messagebox.showerror("Error", "Ha habido un error, por favor, escribe la descripción de la tarea")
    elif not nombre and descripcion:
        messagebox.showerror("Error", "Ha habido un error, por favor, escribe el nombre de la tarea")
    else:
        messagebox.showwarning("Cuidado", "Ha habido un fallo, rellena los campos necesarios")

# Función para crear notas
def crearNotas():
    contenido = entrada_notas.get("1.0", END).strip() # Contenido de la nota
        
    # Comprobar si el campo está completo o no y guardar en caso positivo
    if contenido is None:
        messagebox.showerror("Alerta", "Tienes que rellenar este campo obligatoriamente")
    else:
        with open("notas.txt", "a") as archivo_notas:
            archivo_notas.write(f"\n  Nota: {contenido}\n\n")
            messagebox.showinfo("Exito", "Tu nota se a guardado correctamente")

# Función para crear recordatorios
def crearRecordatorios():
    nombreRecordatorio = entry_nombre_recordatorio.get() # Nombre del recordatorio
    fecha = entry_fecha_recordatorio.get() # Fecha del recordatorio
        
    # Comprobar si los campos están completos o no y guardar en caso positivo
    if nombreRecordatorio and fecha:
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y").date()
            with open("recordatorios.txt", "a") as archivo_recordatorios:
                archivo_recordatorios.write(f"\nRecordatorio: {nombreRecordatorio}\nFecha: {fecha}\n\n")
            messagebox.showinfo("Éxito", f"Recordatorio '{nombreRecordatorio}' guardado para el día: {fecha}")
        except ValueError:
            messagebox.showerror("Error", "La fecha no es correcta, por favor usa el formato dd/mm/yyyy")
    elif nombreRecordatorio and not fecha:
        messagebox.showerror("Error", "Por favor, ingresa la fecha del recordatorio")
    elif not nombreRecordatorio and fecha:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del recordatorio")
    else:
            messagebox.showwarning("Cuidado", "Ha habido un fallo, rellena los campos necesarios")

# Función para eliminar la tarea
def eliminarTarea():
    nombre_tarea_eliminar = entry_nombre_tarea.get()

    # Lógica para eliminar la tarea y en caso de no encontrarse, da mensajes de error o de fallo
    if nombre_tarea_eliminar:
        with open("tareas.txt", "r") as archivo_tareas:
            lineas = archivo_tareas.readlines()
        with open("tareas.txt", "w") as archivo_tareas:
            tarea_encontrada = False
            for i in range(0, len(lineas), 3):
                if nombre_tarea_eliminar not in lineas[i]:
                    archivo_tareas.writelines(lineas[i:i+3])
                else:
                    tarea_encontrada = True
            if tarea_encontrada:
                messagebox.showinfo("Éxito", f"Tarea '{nombre_tarea_eliminar}' eliminada.")
            else:
                messagebox.showerror("Error", f"No se encontró una tarea con el nombre '{nombre_tarea_eliminar}'.")
    elif not nombre_tarea_eliminar:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea que deseas eliminar")
    else:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la tarea que deseas eliminar")
    
# Función para eliminar una nota
def eliminarNota():
    nombreNotaEliminar = entry_eliminar_nota.get()

    # Lógica para eliminar la nota y en caso de no encontrarse, da mensajes de error o de fallo
    if nombreNotaEliminar:
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
                messagebox.showerror("Error", f"No se encontró una nota con '{nombreNotaEliminar}'.")
    elif not nombreNotaEliminar:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la nota que deseas eliminar")
    else:
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la nota que deseas eliminar")

# Función para eliminar un recordatorio
def eliminarRecordatorio():

    # Lógica para eliminar el recordatorio y en caso de no encontrarse, se muestra un mensaje de error o de fallo
    nombre_recordatorio_eliminar = entry_eliminar_recordatorio.get()

    if nombre_recordatorio_eliminar:
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
                messagebox.showerror("Error", f"No se encontró un recordatorio con el nombre '{nombre_recordatorio_eliminar}'.")
    elif not nombre_recordatorio_eliminar:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del recordatorio que deseas eliminar")
    else:
        messagebox.showerror("Error", "Por favor, ingresa el nombre del recordatorio que deseas eliminar")

# Selección de la acción que quiere hacer el usuario
def seleccion():
    accion = accion_var.get()
    if accion == "crear":
        frame_crear.grid(fill="both", expand=True)
        frame_eliminar.pack_forget()
    elif accion == "eliminar":
        frame_eliminar.grid(fill="both", expand=True)
        frame_crear.pack_forget()


#LÓGICA PARA QUE SE IMPRIMA UNA VENTANA EN PANTALLA CON LA QUE EL USUARIO PUEDA INTERACTUAR
pantalla = Tk()
pantalla.configure(background="#D6D5C2")
pantalla.title("Notas, Recordatorios y Tareas")
pantalla.geometry("800x600")

# Opciones para crear o eliminar
accion_var = tk.StringVar(value="crear")
frame_eliminar = tk.Frame(pantalla)
frame_crear = tk.Frame(pantalla)

# Tarea
label_nombre_tarea = tk.Label(frame_crear, text="Nombre de la tarea:")
label_nombre_tarea.grid()
entry_nombre_tarea = tk.Entry(frame_crear)
entry_nombre_tarea.grid()

label_descripcion_tarea = tk.Label(frame_crear, text="Descripción de la tarea:")
label_descripcion_tarea.grid()
entry_descripcion_tarea = tk.Entry(frame_crear)
entry_descripcion_tarea.grid()

boton_crear_tarea = tk.Button(frame_crear, text="Crear tarea", command=crearTarea)
boton_crear_tarea.grid()

# Recordatorio
label_nombre_recordatorio = tk.Label(frame_crear, text="Nombre del recordatorio:")
label_nombre_recordatorio.grid()
entry_nombre_recordatorio = tk.Entry(frame_crear)
entry_nombre_recordatorio.grid()

label_fecha_recordatorio = tk.Label(frame_crear, text="Fecha (dd/mm/yyyy):")
label_fecha_recordatorio.grid()
entry_fecha_recordatorio = tk.Entry(frame_crear)
entry_fecha_recordatorio.grid()

boton_crear_recordatorio = tk.Button(frame_crear, text="Crear recordatorio", command=crearRecordatorios)
boton_crear_recordatorio.grid()

# Nota
label_nombre_nota = tk.Label(frame_crear, text="Nombre de la nota:")
label_contenido_nota = tk.Label(frame_crear, text="Contenido de la nota:")
label_nombre_nota.grid()
label_contenido_nota.grid()
entry_nombre_nota = tk.Entry(frame_crear)
entry_contenido_nota = tk.Entry(frame_crear)
entry_nombre_nota.grid()
entry_contenido_nota.grid()
boton_crear_nota = tk.Button(frame_crear, text="Crear nota", command=crearNotas)
boton_crear_nota.grid()
#zdadadacaadadaaadaad

pantalla.mainloop()