
from Managers.errManager import catalogoErrores
from Managers.prtManager import editPrintLogger
# Ingresa una posicion y un valor para que se retorne su tipo
def getTypeVal(pos, val):
    pos = round((int(pos) / 1000)) % 4
    if val is None:
        return val
    if pos == 0:
        
        return (int(float(val)))
    elif pos == 1:
        return (float(val))
    elif pos == 2:
        return (val)
    else:
        if val == "True":
            return (bool(True))
        else:
            return (bool(False))

#Agarrar la memoria del pointer
def getPointer(memaux,temp):
    memaux = memaux.replace("(","")
    memaux = memaux.replace(")","")
    mempos = str(temp[str(memaux)])
    return mempos
# Si es un pointer asignarle la su repectivo valor de memoria 
def checkPointer(memVal,temp):
    if "(" in memVal:
        return getPointer(memVal,temp)
    else:
        return  memVal
        
# Si es operador vamos a resolver problema
def solveExpesion(op, p):
    if op == '+':
        return  p[0] + p[1]
    elif op == '-':   
        return  p[0] - p[1]
    elif op == '*':
        return  p[0] * p[1]
    elif op == '/':
        return  p[0] / p[1]
    elif op == '<':
        return  p[0] < p[1]
    elif op == '>':
        return  p[0] > p[1] 
    elif op == '<=':
        return  p[0] <= p[1]
    elif op == '>=': 
        return  p[0] >= p[1] 
    elif op == '||':
        if p[0] or p[1]:
            return  True
        else:
            return  False  
    elif op == '&&':
        if p[0] and p[1]:
            return  True
        else:
            return  False  
    elif op == '==':
        return  p[0] == p[1]    
    elif op == '%':      
        return  p[0] % p[1]


# Funcion que recibe el punto de memoria y retorna su tipo
def getMemoryModule(address):
    if isinstance(address, str):
        address = int(address)

    if address >= 0 and address <= 3999:         
        return "constante"
    elif address >= 4000 and address <= 7999:
        return "local"
    elif address >= 8000 and address <= 11999 :
        return "global"
    else:
        return "temporal"

# FUncion que recibe la dirrecion de memoria, su valor y le asigna el tipo correcto. Retorna este valor
def getMemoryType(addresVal, val):
    # Calculo para predecir el tipo

    addrsNumber = round(int(addresVal) / 1000) % 4
    try:
        if addrsNumber ==  0:
            if val == '-0.0':
                val = '0'
            val = int(float(val))         
        elif addrsNumber == 1:
            val = float(val)
        elif addrsNumber == 2:
            val = str(val)
        elif addrsNumber == 3:
            if val == 'False':
                val = False
            else:
                val = True
    except:
        catalogoErrores([13, val, type(val)])
    return val

# Funcion para correr la maquina virtual
# Recibimos los cuadruplos, el directorio de funciones y la tabla de constantes
def runVM(cuadruplos, dirFunc, memoriaConst):
    # Declaramos los posibles operadores
    operadores = ['&&', '||', '<', '>', '==', '>=', '<=', '+', '-', '*', '/', '%']
    # Inicializamos las funciones a utlizar
    for item in dirFunc:
        if item != 'global':
            dirFunc["global"][dirFunc[item]["Memoria"]] = None
    # Inicializamos el contador de posicion
    count = 0
    # Generamos el diccionario para la memoria global: variables globales
    memoriaGlobal = dirFunc["global"]
    #memoriaGlobal.update(memoriaConst)
    # Generamos la memoria local (pila por si se anida)
    memoriaLocal = []
    # Inicializamos la memoria temporal
    memoriaTemp = {}
    # Inicializamos la pila de saltos
    returnLoc = []
    # Inicializamos pila de funciones
    # Siempre comenzamos en principal = global
    currentFunc = ['global']
    while cuadruplos[count].op != "END":
        # Primer cuadruplo siempre es gotomain
        if cuadruplos[count].op == "GOTOMAIN":
            # Salta al main
            count = int(cuadruplos[count].top) 
            
        # Si es un operador  
        elif cuadruplos[count].op in operadores:
            # Operaciones
            # Revisamos algun valor es pointer 
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            rightPointer = checkPointer(cuadruplos[count].rightop,memoriaTemp)
            leftPointer = checkPointer(cuadruplos[count].leftop,memoriaTemp)
            
            pointers = []
            # Obtenemos el valor de la memoria
            for item in [int(rightPointer), int(leftPointer)]:
                memoryType = getMemoryModule(item)
                if memoryType == "constante":
                    val = getMemoryType(int(item), memoriaConst[str(item)])        
                elif memoryType == "local": 
                    val = getMemoryType(int(item), memoriaLocal[-1][str(item)]) 
                elif memoryType == "global":
                    val = getMemoryType(int(item), memoriaGlobal[str(item)]) 
                else:
                    val = getMemoryType(int(item), memoriaTemp[str(item)]) 
                pointers.append(val)
            # Asignamos la memoria en un su pila correcta
            memoryType = getMemoryModule(topPointer)
            if memoryType == "constante":         
                memoriaConst[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            elif memoryType == "local": 
                memoriaLocal[-1][topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            elif memoryType == "global":
                memoriaGlobal[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            else:
                memoriaTemp[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            count += 1
        # Asignacion
        elif cuadruplos[count].op == "=":
            # Revisamos algun valor es pointer arreglo
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            rightPointer = checkPointer(cuadruplos[count].rightop,memoriaTemp)
            # Obtenemos el modulo de memoria del pointer        
            memoryType = getMemoryModule(rightPointer)
            if memoryType == "constante":         
                aux = memoriaConst[rightPointer]
            elif memoryType == "local": 
                aux = memoriaLocal[-1][rightPointer]
            elif memoryType == "global":
                aux = memoriaGlobal[rightPointer]
            else:
                aux = memoriaTemp[rightPointer]

            # Asignamos el valor obtenido en la funcion pasada al modulo apropiado
            memoryType = getMemoryModule(topPointer)
            if memoryType == "constante":         
                memoriaConst[topPointer] = aux
            elif memoryType == "local": 
                memoriaLocal[-1][topPointer] = aux
            elif memoryType == "global":
                memoriaGlobal[topPointer] = aux
            else:
                memoriaTemp[topPointer] = aux
            # Incrementamos el contado
            count += 1
        # Imprimr
        elif cuadruplos[count].op == "print":
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            # Revisamos de cual modulo de memoria vamos a sacar el valor y lo mandamos al logger para imprimr
            memoryType = getMemoryModule(topPointer)
            if memoryType == "constante":  
                editPrintLogger(memoriaConst[topPointer])       
            elif memoryType == "local": 
                editPrintLogger(memoriaLocal[-1][topPointer])
            elif memoryType == "global":
                editPrintLogger(memoriaGlobal[topPointer])
            else:
                editPrintLogger(memoriaTemp[topPointer])
            count += 1

            
        elif cuadruplos[count].op == "return":
            # Revisamos algun valor es pointer arreglo
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            memoryType = getMemoryModule(cuadruplos[count].top)
            # Revisamos que tipo de memoria tiene el valor a retornar
            if memoryType == "constante":         
                aux = memoriaConst[topPointer]
            elif memoryType == "local": 
                aux = memoriaLocal[-1][topPointer]
            elif memoryType == "global":
                aux = memoriaGlobal[topPointer]
            else:
                aux = memoriaTemp[topPointer]
            # Retornamos el valor a la funcion
            memoriaGlobal[dirFunc[currentFunc[-1]]["Memoria"]] = aux
            currentFunc.pop()
            memoriaLocal.pop()
            count = returnLoc.pop()
        elif cuadruplos[count].op == "lee":
            memoriaTemp[cuadruplos[count].top] = input()

            count += 1

        # en los gotos asignamos al contador con el salto correspondiente
        elif cuadruplos[count].op == "Goto":
            count = int(cuadruplos[count].top)

        elif cuadruplos[count].op == "GotoF":
            # Revisamos de que modulo vamos  a sacar la memoria,  de ahi vemos si da el salto
            memoryType = getMemoryModule(int(cuadruplos[count].rightop))
            if memoryType == "constante":         
                ifFalse = (memoriaConst[cuadruplos[count].rightop] == False)
            elif memoryType == "local": 
                ifFalse = (memoriaLocal[-1][cuadruplos[count].rightop] == False)
            elif memoryType == "global":
                ifFalse = (memoriaGlobal[cuadruplos[count].rightop] == False)
            else:
                ifFalse = (memoriaTemp[cuadruplos[count].rightop] == False)

            # Si salta agarra el valor del cuadruplo
            if (ifFalse):
                count = int(cuadruplos[count].top)
            else:
                count += 1  


        elif cuadruplos[count].op == "GotoV":
            #si es falso actualizar el contador a el salto correspondiente
            # Revisamos de que modulo vamos  a sacar la memoria,  de ahi vemos si da el salto
            memoryType = getMemoryModule(int(cuadruplos[count].rightop))
            if memoryType == "constante":         
                ifTrue = memoriaConst[cuadruplos[count].rightop]
            elif memoryType == "local": 
                ifTrue = memoriaLocal[-1][cuadruplos[count].rightop]
            elif memoryType == "global":
                ifTrue = memoriaGlobal[cuadruplos[count].rightop]
            else:
                ifTrue = memoriaTemp[cuadruplos[count].rightop]

            # Si salta agarra el valor del cuadruplo
            if (ifTrue):
                count = int(cuadruplos[count].top)
            else:
                count += 1  
            
        # A cada parametro se lo igualamos a una nueva memorialocal
        elif cuadruplos[count].op == "PARAMETER":
            # Ingresamos una dimensiona a la memoria local
            memoriaLocal.append({})
            paramString = "par" + str(paramCounter)
            # Contamos en que parametro vamos para asignar el correcto
            paramCounter += 1
            # Obtenemos el modulo al que se le asignara el parametro
            memoryType = getMemoryModule(cuadruplos[count].rightop)
            if memoryType == "constante":         
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaConst[cuadruplos[count].rightop]
            elif memoryType == "local": 
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaLocal[-2][cuadruplos[count].rightop]
            elif memoryType == "global":
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaGlobal[cuadruplos[count].rightop]
            else:
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaTemp[cuadruplos[count].rightop]
            count += 1
        # Salto a funcion
        elif cuadruplos[count].op == "GOSUB":
            # Ingresamos a donde vamos a regresar con el return o endfunc
            returnLoc.append(count + 1)
            # Salto
            count = int(cuadruplos[count].top) + 1
        
        elif cuadruplos[count].op == "VERIFY":
            memoryType = getMemoryModule(cuadruplos[count].rightop)
            if memoryType == "constante":         
                val = int(memoriaConst[cuadruplos[count].rightop])
            elif memoryType == "local": 
                val= int(memoriaLocal[-1][cuadruplos[count].rightop])
            elif memoryType == "global":
                val = int(memoriaGlobal[cuadruplos[count].rightop])
            else:
                val = int(memoriaTemp[cuadruplos[count].rightop])

            if val >= int(cuadruplos[count].leftop) and val <= int(cuadruplos[count].top):
                count += 1
            else:
                catalogoErrores([12, memoriaConst[cuadruplos[count].rightop]])
            
        elif cuadruplos[count].op == "ERA":
            # Memory activation 
            paramCounter = 0
            currentFunc.append(cuadruplos[count].top)
            count += 1
        elif cuadruplos[count].op == "ENDFUNC":
            # Funcion void
            # Regresamos a punto original
            currentFunc.pop()
            memoriaLocal.pop()
            count = returnLoc.pop()
        else:
            # Error
            catalogoErrores([11])

    