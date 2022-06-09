def createPrintLogger():
    f = open("printLogger.txt", "w")
    return f

def editPrintLogger(newLine):
    f = open("printLogger.txt", "a")
    print("Escribiendo", newLine)
    f.write(str(newLine) + "\n")
    f.close()

def readPrinterLogger():
    f = open("printLogger.txt", "r")
    return f