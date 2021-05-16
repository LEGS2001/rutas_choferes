def cargarDatos():
    global rutas
    dicc = {}
    dicc2 = {}
    datos = []
    fechas = []
    choferes = []
    rutas = []
    choferes_fecha = []
    choferes_unicos = []
    diccionario_choferes = {}

    #Pasa por cada linea del archivo y crea listas de los datos
    archivo = open('C:\\Users\\LUISEMILIO\\Desktop\\Colegio\\UEES\\Fundamentos de Programacion\\Proyecto Parcial 2\\rutasManejadas2020.txt', 'r')
    for linea in archivo:
        dato = linea.split(",")
        dato[2] = dato[2].strip('\n')
        if dato[2] not in fechas:
            fechas.append(dato[2])
        choferes.append(dato[1])
        datos.append(dato)
        rutas.append(dato[0])
    archivo.close

    #Separa los choferes y su ruta en listas segun la fecha en la que viajan Ej: (17-05-2018)[SMS, Guayaquil-Daule, SMZ, Guayaquil-Cuenca], (18-05-2018)[AGB, Guayaquil-Cuenca]
    for i in range(len(fechas)):
        choferes_fecha.append([])
        for j in range(len(datos)):
            if fechas[i] == datos[j][2]:
                choferes_fecha[i].append(datos[j][1])
                choferes_fecha[i].append(datos[j][0])
    
    #Toma la ruta de cada lista creada en el bloque anterior y la pone en un diccionario {Ruta:[Choferes]}
    for i in range(len(choferes_fecha)):
        diccionario_choferes_copia = diccionario_choferes.copy()
        for j in range(len(choferes_fecha[i])):
            if j % 2 != 0:        
                diccionario_choferes_copia.setdefault(choferes_fecha[i][j],[]).append((choferes_fecha[i][j-1]))

        #Toma los valores del diccionario anterior y los guarda en una lista
        chofer_grupo_fecha = list(diccionario_choferes_copia.values())
        for k in range(len(chofer_grupo_fecha)):
            choferes_unicos.append(chofer_grupo_fecha[k])

    #Crea un diccionario {Fecha:{}}, y a la clave (con formato de diccionario) del diccionario anterior guarda las rutas que corresponden a cada fecha, dejandolo como {Fecha:{Ruta:[]}}
    for i in range (len(fechas)):
        dicc2_copia = dicc2.copy()
        dicc[fechas[i]] = dicc2_copia
        for j in range(len(datos)):
            if fechas[i] in datos[j]:             
                dicc2_copia[datos[j][0]] = []

    #Recorre el diccionario creado anteriormente con formato {Fecha:{Ruta:[]}}, y les guarda el valor de los choferes correspondiendo a la clave de cada ruta
    contador = 0
    for fecha, ruta in dicc.items():
        for chofer in ruta:
            dicc[fecha][chofer] = choferes_unicos[contador]
            contador += 1
    print(dicc)
    return dicc

def encontrarChoferes(dicc):
    global ruta_no_manejada
    global fecha_nombre_archivo
    global dias_anteriores
    fechas_anteriores = []
    rutas_no_manejadas_lista = []
    choferes_disponibles = []
    fecha = input("Ingrese la fecha (Formato: DD-MM-AAAA) \n")
    fecha_nombre_archivo = fecha
    dias_anteriores = int(input("Ingrese el numero de dias anteriores que quiere revisar \n"))
    ruta_no_manejada = input("Ingrese la ruta que desea verificar \n")

    #Crea una lista con todas las fechas anteriores en n dias
    for i in range(dias_anteriores):
        fecha_lista = fecha.split("-")
        for i in range(len(fecha_lista)):
            fecha_lista[i] = int(fecha_lista[i])
        if fecha_lista[0] > 0:
            fecha_lista[0] -= 1 
        elif fecha_lista[0] <= 0:
            fecha_lista[0] = 30
            fecha_lista[1] -= 1
        if fecha_lista[1] <= 0:
            fecha_lista[1] = 12
            fecha_lista[2] -= 1
        for i in range(len(fecha_lista)):
            fecha_lista[i] = str(fecha_lista[i])
            if len(fecha_lista[i]) == 1:
                fecha_lista[i] = ("0" + fecha_lista[i])
        fecha_lista = "-".join(fecha_lista)
        fecha = fecha_lista
        fechas_anteriores.append(fecha_lista)

    #Revisa la ruta que no ha sido manejada anteriormente
    for i in rutas:
        if i != ruta_no_manejada and i not in rutas_no_manejadas_lista:
            rutas_no_manejadas_lista.append(i)  

    #Adquiere los valores de los choferes que no han manejado en una ruta especifica, en los dias anteriores
    for i in range(len(fechas_anteriores)):
        for j in range(len(rutas_no_manejadas_lista)):
            try:
                choferes_disponibles.append(dicc[fechas_anteriores[i]][rutas_no_manejadas_lista[j]])
            except:
                pass
    print(choferes_disponibles)
    return choferes_disponibles

#Crea el archivo con los datos de la funcion Encontrar Choferes
def rutasDisponibles():
    try:
        nombre_archivo_final = ruta_no_manejada + "_" + fecha_nombre_archivo + ".txt"
        archivo_final = open('C:\\Users\\LUISEMILIO\\Desktop\\Colegio\\UEES\\Fundamentos de Programacion\\Proyecto Parcial 2\\%s' %nombre_archivo_final, 'w')
        archivo_final.write("Para la ruta ")   
        archivo_final.write(str(ruta_no_manejada))
        archivo_final.write("\nlos choferes disponibles para la fecha ")
        archivo_final.write(str(fecha_nombre_archivo))
        archivo_final.write("\nque no haya manejado ")
        archivo_final.write(str(dias_anteriores))
        archivo_final.write(" dias antes son: ")
        archivo_final.write(str(choferes_disponibles))
        archivo_final.close()
    except:
        print("No se han realizado los pasos anteriores")

#Menu
while True:
    print("1)Cargar Datos \n2)Encontrar Choferes \n3)Crear archivo \n4)Salir")
    opcion = int(input("Ingrese el numero de la opcion deseada \n"))
    if opcion == 1:
        dicc = cargarDatos()
    elif opcion == 2:
        choferes_disponibles = encontrarChoferes(dicc)
    elif opcion == 3:
        rutasDisponibles()
    else:
        break
