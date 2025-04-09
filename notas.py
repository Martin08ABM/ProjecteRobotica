from datetime import datetime

# Pregunta principal para saber qué quiere hacer el usuario
eleccion = input(" 1. Crear/eliminar una tarea\n 2. Añadir/eliminar un recordatorio \n 3. Añadir/eliminar una nota \n¿Qué quieres hacer? Elige un numero: ")

# Crear tarea o eliminar tarea
if eleccion.lower() == "1":
    accion = input("\n  ¿Quieres crear o eliminar una tarea? (crear/eliminar): ").lower()

    if accion == "crear":
        nombre_tarea = input("\n    Nombre de la tarea: ")
        descripcion_tarea = input("\n    Descripcion de la tarea: ")

        with open("tareas.txt", "a") as archivo_tareas:
            archivo_tareas.write(f"\nTarea: {nombre_tarea}\nDescripción: {descripcion_tarea}\n\n")

        print(f"\nTarea '{nombre_tarea}' ha sido agregada y guardada")

    elif accion == "eliminar":
        nombre_tarea_eliminar = input("\n    ¿Qué tarea quieres eliminar? (Escribe el nombre de la tarea): ")
        
        # Eliminar tareas
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
                print(f"\nTarea '{nombre_tarea_eliminar}' eliminada.")
            else:
                print(f"\nNo se encontró una tarea con el nombre '{nombre_tarea_eliminar}'.")

# Añadir o eliminar recordatorio
elif eleccion == "2":
    accion = input("\n  ¿Quieres añadir o eliminar un recordatorio? (crear/eliminar): ").lower()

    # Añadir un recordatorio
    if accion == "crear":
        nombre_recordatorio = input("\n     Nombre del recordatorio: ")
        dia_finalizacion = input("\n    Día para que quieres que acabe (dd/mm/yyyy): ")

        try:
            fecha = datetime.strptime(dia_finalizacion, "%d/%m/%Y").date()

            with open("recordatorios.txt", "a") as archivo_recordatorios:
                archivo_recordatorios.write(f"Recordatorio: {nombre_recordatorio}\nFecha: {fecha}\n\n")

            print(f"\nRecordatorio '{nombre_recordatorio}' guardado para el día: {fecha}")

        except ValueError:
            print("\nLa fecha no es correcta, por favor usa el formato dd/mm/yyyy")

    elif accion == "eliminar":
        nombre_recordatorio_eliminar = input("\n¿Qué recordatorio quieres eliminar? (Escribe el nombre del recordatorio): ")

        # Eliminar recordatorios
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
                print(f"\nRecordatorio '{nombre_recordatorio_eliminar}' eliminado.")
            else:
                print(f"\nNo se encontró un recordatorio con el nombre '{nombre_recordatorio_eliminar}'.")

# Añadir o eliminar nota
elif eleccion == "3":
    accion = input("\n  ¿Quieres añadir o eliminar una (crear/eliminar): ").lower()

    # Añadir una nota
    if accion == "crear":
        nota = input("\n    Escribe tu nota: ")

        with open("notas.txt", "a") as archivo_notas:
            archivo_notas.write(f"\n  Nota: {nota}\n\n")

        print("\nNota guardada")

    elif accion == "eliminar":
        nota_eliminar = input("\n    ¿Qué nota quieres eliminar? (Escribe el contenido de la nota): ")

        # Eliminar notas
        with open("notas.txt", "r") as archivo_notas:
            lineas = archivo_notas.readlines()

        with open("notas.txt", "w") as archivo_notas:
            nota_encontrada = False
            for i in range(0, len(lineas), 2):
                if nota_eliminar not in lineas[i]:
                    archivo_notas.writelines(lineas[i:i+2])
                else:
                    nota_encontrada = True

            if nota_encontrada:
                print(f"\nNota eliminada.")
            else:
                print(f"\nNo se encontró una nota con '{nota_eliminar}'.")

else:
    print("La entrada no es correcta")
