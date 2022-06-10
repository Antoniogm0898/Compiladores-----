from Managers.semManager import cuadruplos
from Managers.errManager import catalogoErrores

def writeOBJ(filename, obj):
    # Creamos el archivo
    new_file=open(filename,mode="w",encoding="utf-8")
    # Primero agregamos el codigo intermedio (cuadruplos)
    new_file.write("CODIGO INTERMEDIO" + "\n")
    for item in obj[0]:
        cuadrStr = str(item.op) + "," + str(item.rightop) + "," + str(item.leftop) + "," + str(item.top) + "\n"
        new_file.write(cuadrStr)

    # Pasamos solamente la memoria en el directorio de funciones.
    # En caso de ser funcion tambien pasamos el numero de parametros, variables locales y temporales
    new_file.write("DIRECTORIO DE FUNCIONES" + "\n")
    for function in obj[1]:
        if obj[1][function]["Type"] == "program":
            new_file.write("global" + "\n")
            for value in obj[1][function]["Vars"]:
                new_file.write(str(obj[1][function]["Vars"][value]["Memoria"]) + "\n")    
        else:
            new_file.write("funcion " + function +"\n")
            new_file.write("Memoria " + str(obj[1][function]["Memoria"]) +"\n")
            new_file.write("Vars " + str(obj[1][function]["Vars"]) + "\n")
            auxString = ""
            for item in obj[1][function]["Param Table"]:
                auxString = item + ", "
            new_file.write("ParamTable " + str(auxString )+ "\n")
            new_file.write("#VL " + str(obj[1][function]["# VL"]) + "\n")
            new_file.write("#VT " + str(obj[1][function]["# VT"]) + "\n")

    # Finalmente pasamos la tabla de constantes
    new_file.write("TABLA DE CONSTANTES" + "\n")
    for value in obj[2]:
        new_file.write(str(value) + ","  + str(obj[2][value][value]) + "\n")

    new_file.close()  

def readOBJ(filepath):
    try:
        datos = open(filepath).read()

        # Flags para dividir el documento
        cuadFlag = False
        dirFlag = False
        constFalg = False
        enter = True

        # Generamos las lineas
        lineas = datos.splitlines()
        
        # Vamos a crear las estructuras de datos
        cuadArr = []
        dirFunc = {"global" : {}}
        consTable = {}
        currentFunc = ""

        for linea in lineas:
            # Cada vez que cambia de segmento levanta una bandera
            enter = True
            if linea == "CODIGO INTERMEDIO":
                cuadFlag = True
                enter = False

            if linea == "DIRECTORIO DE FUNCIONES":
                cuadFlag = False
                dirFlag = True
                enter = False

            if linea == "TABLA DE CONSTANTES":
                dirFlag = False
                constFalg = True
                enter = False

            # Cuadruplos
            if cuadFlag and enter:
                splitLine = linea.split(",")
                cuadArr.append(cuadruplos(splitLine[0], splitLine[1], splitLine[2], splitLine[3]))
            
            # Directorio de funciones
            if dirFlag and enter:
                

                splitLine = linea.split(" ")
                if currentFunc == "global":
                    dirFunc["global"][splitLine[0]] = None
                elif (splitLine[0] != "funcion") and (len(splitLine) > 1):
                    dirFunc[currentFunc][splitLine[0]] = splitLine[1]

                if splitLine[0] == "global":
                    currentFunc = "global"

                if splitLine[0] == "funcion":
                    varCounter = 0
                    currentFunc = splitLine[1]
                    dirFunc[currentFunc] = {}

                if splitLine[0] == "Vars":
                    for item in splitLine:
                        if """'""" not in item and item != "Vars":
                            auxItem = item.replace('}', '')
                            dirFunc[currentFunc]["par" +str(varCounter)] = auxItem.replace(',', '')
                            varCounter += 1

            # Tabla de constantes
            if constFalg and enter:
                splitLine = linea.split(",")
                consTable[splitLine[0]] = splitLine[1]
    except:
        catalogoErrores([9])

    return cuadArr, dirFunc, consTable

def onlyOBJ(lineas):
    try:
        # Flags para dividir el documento
        cuadFlag = False
        dirFlag = False
        constFalg = False
        enter = True
        
        # Vamos a crear las estructuras de datos
        cuadArr = []
        dirFunc = {"global" : {}}
        consTable = {}
        currentFunc = ""

        for linea in lineas:
            # Cada vez que cambia de segmento levanta una bandera
            enter = True
            if linea == "CODIGO INTERMEDIO":
                cuadFlag = True
                enter = False

            if linea == "DIRECTORIO DE FUNCIONES":
                cuadFlag = False
                dirFlag = True
                enter = False

            if linea == "TABLA DE CONSTANTES":
                dirFlag = False
                constFalg = True
                enter = False

            # Cuadruplos
            if cuadFlag and enter:
                splitLine = linea.split(",")
                cuadArr.append(cuadruplos(splitLine[0], splitLine[1], splitLine[2], splitLine[3]))
            
            # Directorio de funciones
            if dirFlag and enter:
                

                splitLine = linea.split(" ")
                if currentFunc == "global":
                    dirFunc["global"][splitLine[0]] = None
                elif (splitLine[0] != "funcion") and (len(splitLine) > 1):
                    dirFunc[currentFunc][splitLine[0]] = splitLine[1]

                if splitLine[0] == "global":
                    currentFunc = "global"

                if splitLine[0] == "funcion":
                    varCounter = 0
                    currentFunc = splitLine[1]
                    dirFunc[currentFunc] = {}

                if splitLine[0] == "Vars":
                    for item in splitLine:
                        if """'""" not in item and item != "Vars":
                            auxItem = item.replace('}', '')
                            dirFunc[currentFunc]["par" +str(varCounter)] = auxItem.replace(',', '')
                            varCounter += 1

            # Tabla de constantes
            if constFalg and enter:
                splitLine = linea.split(",")
                consTable[splitLine[0]] = splitLine[1]
    except:
        catalogoErrores([9])

    return cuadArr, dirFunc, consTable