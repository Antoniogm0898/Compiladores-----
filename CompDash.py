from LexerParser import runLexerParser
#from VirtualMachine import runVM
from Managers.objManager import readOBJ, writeOBJ, onlyOBJ
from Managers.prtManager import editPrintLogger
from VirtualMachine import runVM
import os

memoria = []

# Ejecucion del codigo
def runCode(code, generateOBJ, loadedText):
    # Cambios el codigo a TXT y lo parseamos
    text_file = open("AUXTEXCTX.txt", "w")
    text_file.write(code)
    text_file.close()
    
    file = open("AUXTEXCTX.txt", "r")

    fullText =  ""
    for x in file:
        fullText = fullText + x
    file.close()

    os.remove("AUXTEXCTX.txt")

    # Generamos y eliminamos el obj si se pidio
    filename = "NewObj.obj"
    created = False
    cont = 1

    while (not created):
        if os.path.exists(filename):
            filename = "NewObj (" + str(cont) + ").obj"
            cont += 1
        else:
            created = True

    obj = runLexerParser(fullText, memoria)
    writeOBJ(filename, obj)

    if generateOBJ:
        editPrintLogger("Se imprimio de el " + filename + " manera exitosa")
        cuadruplos, dirFunc, consTable = readOBJ(filename)
        runVM(cuadruplos, dirFunc, consTable)
    elif loadedText:
        cuadruplos, dirFunc, consTable = readOBJ(filename)
        runVM(cuadruplos, dirFunc, consTable)
        os.remove(filename)
    else:
        cuadruplos, dirFunc, consTable = readOBJ(filename)
        os.remove(filename)
        # Corremos el codigo 
        runVM(cuadruplos, dirFunc, consTable)


    return fullText, cuadruplos


# Generacion archivo txt
def generateText(code):
    created = False
    cont = 1
    filename = "ProgramFile.txt"
    while (not created):
        if os.path.exists(filename):
            filename = "ProgramFile (" + str(cont) + ").txt"
            cont += 1
        else:
            text_file = open(filename, "w")
            text_file.write(code)
            text_file.close()
            created = True
    editPrintLogger("Impresion exitosa")


def runOBJ(code):
    cuadArr, dirFunc, consTable = onlyOBJ(code)
    runVM(cuadArr, dirFunc, consTable)

    return cuadArr