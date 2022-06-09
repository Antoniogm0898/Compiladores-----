
from Managers.objManager import cuadruplos
from Managers.objManager import readOBJ

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
#agarrar la memoria del pointer
def getPointer(memaux,temp):
    
    memaux = memaux.replace("(","")
    memaux = memaux.replace(")","")
    mempos = str(temp[memaux])
    return mempos
# si es un pointer asignarle la memoria 
def checkPointer(memVal,temp):
    if "(" in memVal:
       
        return getPointer(memVal,temp)
    else:
        return  memVal
# Si es operador vamos a resolver problema
# cuadruplos[count].top, op
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
###############

def getMemoryType(addresVal, val):
    addrsNumber = round(int(addresVal) / 1000) % 4
    if val == None:
        val = addresVal
    if addrsNumber ==  0:
        val = int(float(val))
    elif addrsNumber == 1:
        val = float(val)
    elif addrsNumber == 2:
        val = str(val)
    elif addrsNumber == 3:
        val = bool(val)

        

    return val

def runVM(cuadruplos, dirFunc, consTable):
    c = 0
    operadores = ['&&', '||', '<', '>', '==', '>=', '<=', '+', '-', '*', '/', '%']
    #cuadruplos, dirFunc, consTable = readOBJ("newfile.obj")
    for item in dirFunc:
        if item != 'global':
            dirFunc["global"][dirFunc[item]["Memoria"]] = None
    count = 0
    memoriaGlobal = dirFunc["global"]
    memoriaGlobal.update(consTable)
    memoriaLocal = []
    returnLoc = []
    memoriaTemp = {}

    currentFunc = ['global']
    while cuadruplos[count].op != "END":
        c += 1
        
        if cuadruplos[count].op == "GOTOMAIN":
            count = int(cuadruplos[count].top)
        
        elif cuadruplos[count].op in operadores:
            # Operaciones
            #arreglar ponters --- mandar la tabla de temporales para guardar la dirrecion del pointer
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            rightPointer = checkPointer(cuadruplos[count].rightop,memoriaTemp)
            leftPointer = checkPointer(cuadruplos[count].leftop,memoriaTemp)
            pointers = []
            
            # Obtenemos el valor de la memoria
            for item in [int(rightPointer), int(leftPointer)]:
                memoryType = getMemoryModule(item)
                
                if memoryType == "constante":
                    val = getMemoryType(int(item), consTable[str(item)])          
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
                consTable[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            elif memoryType == "local": 
                memoriaLocal[-1][topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            elif memoryType == "global":
                memoriaGlobal[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            else:
                memoriaTemp[topPointer] = solveExpesion(cuadruplos[count].op, pointers)
            count += 1

        elif cuadruplos[count].op == "=":

            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            rightPointer = checkPointer(cuadruplos[count].rightop,memoriaTemp)

            
            # Asignacion     
        

            memoryType = getMemoryModule(rightPointer)
            if memoryType == "constante":         
                aux = consTable[rightPointer]
            elif memoryType == "local": 
                aux = memoriaLocal[-1][rightPointer]
            elif memoryType == "global":
                aux = memoriaGlobal[rightPointer]
            else:
                aux = memoriaTemp[rightPointer]
            if rightPointer == '12004':
                print("AQUI", aux)
            memoryType = getMemoryModule(topPointer)
            if memoryType == "constante":         
                consTable[topPointer] = aux
            elif memoryType == "local": 
                memoriaLocal[-1][topPointer] = aux
            elif memoryType == "global":
                memoriaGlobal[topPointer] = aux
            else:
                memoriaTemp[topPointer] = aux
            
            
            count += 1

        elif cuadruplos[count].op == "print":
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            memoryType = getMemoryModule(topPointer)
            if memoryType == "constante":         
                print("print",consTable[topPointer])
            elif memoryType == "local": 
                print("print",memoriaLocal[-1][topPointer])
            elif memoryType == "global":
                print("print",memoriaGlobal[topPointer])
            else:
                print("print",memoriaTemp[topPointer])
            count += 1

            
        elif cuadruplos[count].op == "return":
            print("COMENZAMOS", returnLoc[-1], "\n")
            #asignar el return a la memoria de funcion correspondiente e igualar el count para que siga en el cuadruplo siguiente
            topPointer = checkPointer(cuadruplos[count].top,memoriaTemp)
            memoryType = getMemoryModule(cuadruplos[count].top)
            if memoryType == "constante":         
                aux = consTable[topPointer]
            elif memoryType == "local": 
                aux = memoriaLocal[-1][topPointer]
            elif memoryType == "global":
                aux = memoriaGlobal[topPointer]
            else:
                aux = memoriaTemp[topPointer]
            memoriaGlobal[dirFunc[currentFunc[-1]]["Memoria"]] = aux
            memoriaLocal.pop()
            count = returnLoc.pop()
        elif cuadruplos[count].op == "lee":
            count += 1

        # en los gotos asignamos al contador con el salto correspondiente
        elif cuadruplos[count].op == "Goto":
            count = int(cuadruplos[count].top)
          

        elif cuadruplos[count].op == "GotoF":

            memoryType = getMemoryModule(int(cuadruplos[count].rightop))
            if memoryType == "constante":         
                ifFalse = (consTable[cuadruplos[count].rightop] == False)
            elif memoryType == "local": 
                ifFalse = (memoriaLocal[-1][cuadruplos[count].rightop] == False)
            elif memoryType == "global":
                ifFalse = (memoriaGlobal[cuadruplos[count].rightop] == False)
            else:
                ifFalse = (memoriaTemp[cuadruplos[count].rightop] == False)

            if (ifFalse):
                count = int(cuadruplos[count].top)
            else:
                count += 1  


        elif cuadruplos[count].op == "GotoV":
            #si es falso actualizar el contador a el salto correspondiente
            if(memoriaGlobal[cuadruplos[count].rightop] == True):
                count = int(cuadruplos[count].top)
            else:
                count += 1
            
        # A cada parametro se lo igualamos a una nueva memorialocal
        elif cuadruplos[count].op == "PARAMETER":
            memoriaLocal.append({})
            paramString = "par" + str(paramCounter)
            paramCounter += 1
            memoryType = getMemoryModule(cuadruplos[count].rightop)
            if memoryType == "constante":         
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = consTable[cuadruplos[count].rightop]
            elif memoryType == "local": 
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaLocal[-2][cuadruplos[count].rightop]
            elif memoryType == "global":
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaGlobal[cuadruplos[count].rightop]
            else:
                memoriaLocal[-1][dirFunc[currentFunc[-1]][paramString]] = memoriaTemp[cuadruplos[count].rightop]
            count += 1

        elif cuadruplos[count].op == "GOSUB":
            returnLoc.append(count + 1)
            count = int(cuadruplos[count].top) + 1
        
        elif cuadruplos[count].op == "VERIFY":
            count += 1
        elif cuadruplos[count].op == "ERA":
            paramCounter = 0
            currentFunc.append(cuadruplos[count].top)

            count += 1
        elif cuadruplos[count].op == "ENDFUNC":
            print("Entramos a end fun")
            count += 1
            break
        else:
            print(cuadruplos[count].op)
            print("Haz d")

    