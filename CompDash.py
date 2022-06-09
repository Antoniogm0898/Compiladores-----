from LexerParser import runLexerParser
#from VirtualMachine import runVM
from Managers.objManager import readOBJ, writeOBJ
from VirtualMachine import runVM
import os

memoria = []

# Ejecucion del codigo
def runCode(code, generateOBJ):
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

    obj = runLexerParser(fullText, filename, memoria)
    writeOBJ(filename, obj)
    if generateOBJ:
        print("Se imprimio de el obj manera exitosa")
    else:
        cuadruplos, dirFunc, consTable = readOBJ(filename)
        os.remove(filename)
        # Corremos el codigo 
        runVM(cuadruplos, dirFunc, consTable)


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
    print("Impresion exitosa")