
# Generar los valores para la memoria
def generaMemoria(inputs):
    if inputs == []:
        # Memoria estandar
        return [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    else:
        memory = [0]
        for memorySize in inputs:
            memory.append(memorySize + memory[-1])
        return memory

# Obtener el indice de memoria
def returnMemoryType(function, type):

    if function == "global":
        return(type + "Global")
    elif function == "Temp":
        return(type + "Temp")
    elif function == "local":
        return(type + "Local")
    else:
        return(type + "Local")

# Obtenemos el la direccion virtual: Regresamos el valor y actualizamos la memoria
def obtenMemVir(current_func, current_type, memoriaVir, size):
    memoryIndex = returnMemoryType(current_func, current_type)
    result = memoriaVir[memoryIndex]
    memoriaVir[memoryIndex] += size

    return result, memoriaVir

def generaMemoriaConst(indexVal, memoriaVir, type, ptype, pilaO):
    # Obten la direccion
    vm = memoriaVir[indexVal]
    memoriaVir[indexVal] += 1
    # Se agrega el valor a la pila
    pilaO.append(vm)
    if ptype != None:
        # Actualiza el tipo
        ptype.append(type)
        return memoriaVir, ptype, type, pilaO
    else:
        return memoriaVir, memoriaVir[indexVal], pilaO