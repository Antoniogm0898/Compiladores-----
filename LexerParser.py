import ply.lex as lex
import ply.yacc as yacc
from Managers.semManager import newTV, newVar, apply_cubo_semantico, cuadruplos
from Managers.errManager import catalogoErrores
from Managers.memManager import generaMemoria, returnMemoryType, obtenMemVir, generaMemoriaConst
from Managers.prtManager import editPrintLogger

#####################################################################
###################             LEXER             ###################
#####################################################################

# Vamos a crear los tokens para nuestro compilador, para esto nos vamos a apoyar con el lexer de Ply

# Tokens palabras reservadas (El diccionario las convierte de minuscula a mayuscula)
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'elif' : 'ELSEIF',
    'for' : 'FOR',
    'while' : 'WHILE',
    'do' : 'DO',
    'to' : 'TO',
    'programa' : 'PROGRAMA',
    'principal' : 'PRINCIPAL',
    'return' : 'RETURN',
    'lee' : 'LEE',
    'escribir' : 'ESCRIBIR',
    'int'  : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'funcion' : 'FUNCION',
    'void'  : 'VOID',
    'bool' : 'BOOL',
    'atributos': 'ATRIBUTOS',
    'metodos' :'METODOS',  
    'True' : 'TRUE',
    'False' : 'FALSE'
 }

# Agregamos los tokens que se van a definir con regex
tokens = ['ID', 'PLUS' , 'MINUS' ,'MULT','MOD','DIV','EQUALS','COLON','SEMI','COMMA','LPAREN',
         'RPAREN','LBRACKET','RBRACKET','LBRACES','RBRACES','LT', 'LE', 'GT', 'GE', 'EQ',
         'NE','LOR','LAND','CTE_I','CTE_F','CTE_S', 'RANGE'] + list(reserved.values())

# Regex para los tokens
t_ignore = " \t\n"  
t_PLUS = r'\+'
t_MINUS   = r'-'
t_MULT   = r'\*'
t_MOD = r'%'
t_DIV  = r'/'
t_EQUALS = r'='
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACES = r'\{'
t_RBRACES = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LOR = r'\|\|'
t_LAND = r'&&'
t_CTE_I = r'\d+'
t_CTE_F = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_CTE_S = r'\'.*?\''
t_RANGE = r'\.\.'


# Vamos a identificar si es un id o una palabra reservada
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t

def t_error(t):
    catalogoErrores("ERROR: Illegal character " + str(t.value[0]))

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

lex.lex()

#####################################################################
################             ESTRUCTURAS            #################
#####################################################################

# Estructuras para el programa
current_name = None # ID actual
current_type = None # Tipo actual
current_func = [] # Una pila para mostrar la funcion actual
pOper = [""] # Pila de Operandos
pilaO = [] # Pila de Operadores
cuad = [] # Cuadruplos
ptype = [] # Pila de tipos
pjumps = [] # Pila de saltos
pelse = [] # Una pila para el if elif else
saltoselse = []
vControl = 0 ################################################################################# HAY V CONTROLS QUE NO SE USAN
cont = 0 # Contador de posicion actual
countCuad = 0 # Contador para los saltos en ciclos
parameterCounter = 0 # Contador de cantidad de parametros
tempcount = 0 # Contador de cantida de temporales
pParam = [] # Pila con los tipos de los parametros
paramTable = [] # Tabla de parametros 
pCurrentCall = [] # Pila para manejar la llamada actual
constTable = {} # Tabla de constantes
obj = [] # Arreglo para elementos obj (Cuadruplos, dirFun, consTable)
dim = 1
r = 1
pilaDim = []
dimNode = ""
# Vamos a definir las direcciones iniciales para la memoria virtual
# Para cada modulo de memoria se definen los tipos
arraux = None


# Guardamos las dirreciones dentro de un diccionario
memoriaVir = {}

# Guardamos los valores de los temporales para reiniciar la memoria cuando se deba
memoriaTemp = {}

#####################################################################
###################             PARSER            ###################
#####################################################################

# Programa
def p_programa(p):
    '''
    programa : gotomain PROGRAMA addDir ID SEMI programa2
    '''
    # Una vez que termina de correr el programa creamos el OBJ y borramos el directorio de funciones
    global directorio_fun, current_func, ptype
    current_func.pop()
    ptype = []
    cuad.append(cuadruplos("END","","",""))
    obj.append(cuad)
    obj.append(directorio_fun)
    obj.append(constTable)
    del(directorio_fun)

def p_programa2(p):
    '''
    programa2 : atributos programa2
              | programa3
    '''

def p_programa3(p):
    '''
    programa3 : metodos programa3
              | programa4 
    '''

def p_programa4(p):
    '''
    programa4 : setmainloc principal
    '''

# Atributos
def p_atributos(p):
    '''
    atributos : ATRIBUTOS addDir var
    '''

# Metodos
def p_metodos(p):
    '''
    metodos : METODOS funciones
    '''

# Principal
def p_principal(p):
    '''
    principal : PRINCIPAL LPAREN estatutos principal2
    '''
def p_principal2(p):
    '''
    principal2 : estatutos principal2
               | RPAREN
    '''

# Funciones
def p_funciones(p):
    '''
    funciones : tipo funciones2
              | VOID funciones2
    '''  
def p_funciones2(p):

    '''
    funciones2 : FUNCION ID addDir LPAREN addDir parametros RPAREN addParamCount LBRACES addContF atributos funciones3
               | FUNCION ID addDir LPAREN addDir parametros RPAREN addParamCount LBRACES addContF funciones3
               | FUNCION ID addDir LPAREN addDir parametros RPAREN addParamCount LBRACES var addContF funciones3
    '''
def p_funciones3(p):
    '''
    funciones3 : estatutos RBRACES addDir funciones
               | estatutos RBRACES addDir
               | estatutos funciones3
    '''

# Parametros
def p_parametros(p):
    '''
    parametros : tipo ID setCurrentID addValueVarT newParamType COMMA parametros
               | tipo ID setCurrentID addValueVarT newParamType
    '''
    
# Return
def p_retornar(p):
    '''
    retornar : RETURN returnFlag LPAREN retornar2
    '''

def p_retornar2(p):
    '''
    retornar2 : exp cuadRetornar COMMA retornar2
              | exp cuadRetornar RPAREN
    '''

# Variables
def p_var(p):
    '''
    var : tipo COLON var2
    '''

def p_var2(p):
    ''' 
    var2 : ID setCurrentID addValueVarT var3
         | ID setCurrentID addValueVarT LBRACKET newArray CTE_I setL RANGE CTE_I setL var4 
    '''
    
def p_var3(p):
    '''
    var3 : COMMA var2
         | SEMI var
         | SEMI    
    '''
def p_var4(p):
    '''
    var4 : RBRACKET cerrarNodes var3
         | COMMA increaseDim CTE_I setL RANGE CTE_I setL RBRACKET cerrarNodes var3
    '''
# Tipo
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
         | CHAR
         | BOOL
    '''
    # Symbol Table 4. Se agrega el programa al directorio
    global current_type
    current_type = p[1]

# Exp
def p_exp(p):
    '''
    exp : texp checarexp
        | exp addOL exp 
    '''
def p_texp(p):
    '''
    texp : gexp checarexp
         | texp addOL texp
    '''
def p_gexp(p):
    '''
    gexp : mexp checarexp
         | gexp gexp2 gexp
    '''
def p_gexp2(p):
    '''
    gexp2 : LT addO
          | LE addO
          | GT addO
          | GE addO
          | EQ addO
          | NE addO
    '''
def p_mexp(p):
    '''
    mexp : t checarexp
         | mexp mexp2 
    '''
def p_mexp2(p):
    '''
    mexp2 : PLUS addO mexp 
          | MINUS addO mexp 
    ''' 
def p_t(p):
    '''
    t : f checarexp
      | t t2 
    '''
def p_t2(p):
    '''
    t2 : MULT addO t 
       | DIV addO t 
       | MOD addO t 
    '''
def p_f(p):
    '''
    f : LPAREN addFakeBottom exp RPAREN popFakeBottom
      | CTE_I addIntType
      | CTE_F addFloatType
      | CTE_S addCharType
      | TRUE addBoolType
      | FALSE addBoolType
      | llamada
      | ID 
      | ID LBRACKET agregarVar verifyAEx addFakeBottom exp crearCuadA f2 
    '''
    global current_type,current_name, directorio_fun, pilaO, ptype
    # En caso que se este tratando de hacer una llamada o obtener una variable 
    if len(p) == 2 and p[1] != None:
        # Verificamos que la variable exista en la tabla
        if p[1] in directorio_fun[current_func[-1]]["Vars"]:          
            current_name = p[1] 
            # Agregamos la direccion de memoria a la pila
            pilaO.append(directorio_fun[current_func[-1]]["Vars"][p[1]]["Memoria"])
            if p[1] != None:
                # Si el tipo de llamada no es void se agrega el tipo a la pila
                ptype.append(directorio_fun[current_func[-1]]["Vars"][current_name]["Type"])
        else:
            catalogoErrores([7, p[1]])

def p_f2(p):
    '''
    f2 : COMMA updateDim exp crearCuadA RBRACKET crearCuadB popFakeBottom
       | RBRACKET crearCuadB popFakeBottom
    '''
    global current_type, pilaO, pilaDim
    indexVal = returnMemoryType("Temp", current_type)
    pilaO.append("(" + str(memoriaVir[indexVal] - 1) + ")")
    pilaDim.pop()

# Estatutos
def p_estatutos(p):
    '''
    estatutos : estatutos2 estatutos
              | estatutos2 
    '''
def p_estatutos2(p):
    '''
    estatutos2 : asigna
               | llamada
               | lee
               | escribe
               | condicion
               | ciclow
               | ciclof
               | funciones
               | retornar
    '''

# Asigna
def p_asigna(p):
    '''
    asigna : ID EQUALS push_id exp SEMI
           | ID LBRACKET agregarVar verifyAEx addFakeBottom exp crearCuadA f2 EQUALS push_id exp SEMI
    '''
    # Vamos a asignar un "valor" a una direccion virtual
    global countCuad, pilaO, directorio_fun
    # Obtenemos que se asigna y donde. Al igual sacamos el = de la pila
    leftO = pilaO.pop()
    newid = pilaO.pop()
    oper = pOper.pop()
    # Revisamos que exista la dirreccion en el directorio de variables, si no levanta error

    if "(" not in str(newid) and "(" not in str(leftO):
        if p[1] in directorio_fun[current_func[-1]]["Vars"]:
            resultado = directorio_fun[current_func[-1]]["Vars"][newid]["Memoria"]
        else:
            catalogoErrores([7, p[1]])     
        aux = cuadruplos(oper,leftO,"",resultado)
    else:
        try:
            if "(" in str(newid):
                resultado = directorio_fun[current_func[-1]]["Vars"][leftO]["Memoria"]
                aux = cuadruplos(oper, resultado,"",newid)
            else:
                resultado = directorio_fun[current_func[-1]]["Vars"][newid]["Memoria"]
                aux = cuadruplos(oper,leftO,"",resultado)
        except:
            aux = cuadruplos(oper,leftO,"",newid)
    cuad.append(aux)
    countCuad += 1

# Llamada
def p_llamada(p):
    '''
    llamada : ID callFunc LPAREN exp genParameter llamada2
    '''
def p_llamada2(p):
    '''
    llamada2 : COMMA paramCounter exp genParameter llamada2
             | verLastParam RPAREN
    '''

# Lectura
def p_lee(p):
    '''
    lee : LEE LPAREN exp cuadlee lee2
    '''

def p_lee2(p):
    '''
    lee2 : COMMA exp cuadlee lee2
         | RPAREN
    '''

# Escribir
def p_escribe(p):
    '''
    escribe : ESCRIBIR LPAREN exp cuadprint escribe2
    '''
def p_escribe2(p):
    '''
    escribe2 : COMMA exp cuadprint escribe2
             | RPAREN
    '''

# Condicion if else
def p_condicion(p):
    '''
    condicion : IF condicion2
    '''

def p_condicion2(p):
    '''
    condicion2 : LPAREN exp RPAREN genGTF condicion3 ELSEIF genGT condicion2
               | LPAREN exp RPAREN genGTF condicion3 ELSE genGT condicion3 
               | LPAREN exp RPAREN genGTF condicion3 
    '''

def p_condicion3(p):
    '''
    condicion3 : LBRACES estatutos fillGoto RBRACES 
    '''

# Ciclo While
def p_ciclow(p):
    '''
    ciclow : WHILE storeWhile LPAREN exp RPAREN genGTF DO LBRACES estatutos RBRACES fillWhile
           | DO storeWhile LBRACES estatutos RBRACES WHILE LPAREN exp RPAREN genDoWhile
    '''

# Ciclo for
def p_ciclof(p):
    '''
    ciclof : FOR ID addForId EQUALS exp genFor TO exp compFor DO LBRACES estatutos RBRACES actFor
    '''

#def p_ciclof(p):
#    '''
#    ciclof : FOR ciclof2
#    '''

#def p_ciclof2(p):
#    '''
#    ciclof2 : ciclof3 ciclof2
#            | ciclof3
#    '''

#def p_ciclof3(p):
#    '''
#    ciclof3 : ID addForId EQUALS exp genFor TO exp compFor DO LBRACES estatutos RBRACES actFor
#    '''

def p_error(p):
    if p == None:
        editPrintLogger("EOF")
    else:
        catalogoErrores("ERROR: Error en" + str(p.value) + "favor de revisar el codigo")

#####################################################################
##############           PUNTOS NEURALGICOS         #################
#####################################################################

# Creacion de esctucturas: Dirfun
def p_addDir(p):
    '''
    addDir :
    '''
    global directorio_fun, current_func, varTable, current_type, countCuad, memoriaVir, memoriaTemp, tempcount, ptype
    if (p[-1] == "atributos") or (p[-1] == "("):
        # Symbol Table 3 | 10. Crear tabla de variables si no existe
        if directorio_fun[current_func[-1]]["Vars"] == None:
            directorio_fun[current_func[-1]]["Vars"] = newTV()
    elif p[-1] == "programa":
        # PN Symbol Table 1 y 2. Crear directorio de funciones y agregar el programa al directorio
        directorio_fun = {
            "global" : {
                "Type" : "program",
                "Vars" : None
            }
        }
        # Agregamos el valor a current function
        current_func.append("global")
    elif p[-1] == "}" :
        # Symbol Table 12. Borramos la tabla de variables, ya no la ocupamos
        #directorio_fun[current_func[-1]]["Vars"] = None
        # Generar el ENDFUNC
        cuad.append(cuadruplos('ENDFUNC',"","",""))
        countCuad = countCuad + 1 
        # Liberamos la tabla
        #directorio_fun[current_func[-1]]["Vars"] = None
        #reiniciamos el contador de temporales
        directorio_fun[current_func[-1]]["# VT"] = tempcount
        tempcount = 0
        # Una vez que salgamos de la funcion le damos reset al temporal
        for item in memoriaTemp:
            memoriaVir[item] = memoriaTemp[item]
        current_func.pop()
        ptype = []
    elif p[-2] == "funcion": 
        # Symbol Table 7. Prepara la tabla para agregar funcion nueva
        current_func.append(p[-1])
        if p[-3] == "void":
            current_type = p[-3]
        # Symbol table 9. Buscamos por el id en la tabla de valores, si ya existe se arroja error
        try: 
            directorio_fun[current_func[-1]]
            catalogoErrores([1, current_func[-1]])
        except:
            directorio_fun[current_func[-1]] = {
                "Type" : current_type,
                "Vars" : None
            }

            result, memoriaVir = obtenMemVir("global",current_type,memoriaVir,1)
            directorio_fun[current_func[-1]]["Memoria"] = result

# Actualizacion de estructuras
def p_setCurrentID(p):
    '''
    setCurrentID :
    '''
    # Symbol table 4. Marcar cual es el ID actual
    global current_name
    current_name = p[-1]

# Symbol table 5 / 11. Buscamos por el id en la tabla de valores, si ya existe se arroja error
def p_addValueVarT(p):
    '''
    addValueVarT :
    '''

    global directorio_fun, current_func, current_name, current_type, memoriaVir
    
    # Obtenemos la memoria virtual y lo actualizamos
    result, memoriaVir = obtenMemVir(current_func[-1], current_type, memoriaVir, 1)

    # Ingresar la memoria virtual en el directorio de funciones
    directorio_fun[current_func[-1]]["Vars"][current_name] = newVar(directorio_fun[current_func[-1]]["Vars"], current_name, current_type,result)

# Punto neuralgico con funcion de agregar fake bottom (Apoya cambiando el orden de operaciones, flujo, etc)
def p_addFakeBottom(p):
    '''
    addFakeBottom : 
    '''
    pOper.append('[')

# Punto neuralgico con funcion de quitar el fake bottom
def p_popFakeBottom(p):
    '''
    popFakeBottom : 
    '''
    top_val = pOper.pop()
    if top_val != '[':
        catalogoErrores([3])


#############################################################
##############           EXPRESIONES        #################
#############################################################

# Agregar operador
def p_addO(p):
    '''
    addO : 
    '''
    global pOper
    pOper.append(p[-1])

# Agregamos el operador OR y AND
def p_addOL(p):
    '''
    addOL : LOR
          | LAND
    '''
    global pOper
    pOper.append(p[1])

# Crear cuadruplo para los operandos
def p_checarexp(p):
    '''
    checarexp :
    '''
    # Generamos los cuadruplos para las operaciones
    global cont, memoriaVir, current_func,countCuad,tempcount

   
    operadores = ['&&', '||', '<', '>', '==', '>=', '<=', '+', '-', '*', '/', '%']
    if  pOper[-1] in operadores:
            
            # Sacamos de las pilas los operandos derechos, izquierdos y sus tipos
            leftO = pilaO.pop()
            rightO = pilaO.pop()
            leftT = ptype.pop()
            rightT = ptype.pop()

            # Sacamos el operador
            oper = pOper.pop()
            
            # Utlizamos el cubo semantico para validar la operacion entre tipos
            resultType = apply_cubo_semantico(leftT,rightT,oper)
            
            # Si los tipos son inscompatibles regresa error
            if resultType == 'err': 
                catalogoErrores([2, str(leftO) + " : " + leftT, str(rightO) + " : " + rightT])

            # En caso que no haya errores crea el cuadruplo del resultado
            indexVal = returnMemoryType("Temp", resultType)
            result = memoriaVir[indexVal]
            memoriaVir[indexVal] += 1
            tempcount += 1
            cuad.append(cuadruplos(oper,rightO,leftO,result))
            countCuad += 1
            
            # Se agrega a la pila de operadores y tipos
            pilaO.append(result)
            ptype.append(resultType)
            cont += 1

# Si es una constante int, float, char o bool se agregan a su respectivo lugar
# Se genera un indice de memoria para 
def p_addIntType(p):
    '''
    addIntType : 
    '''
    global memoriaVir, ptype, constTable, current_type, pilaO

    # Se genera la direccion virtual apropiada
    memoriaVir, ptype, current_type, pilaO = generaMemoriaConst("intConst", memoriaVir, "int", ptype, pilaO)
    constTable[pilaO[-1]] = {"Type" : current_type, pilaO[-1] : p[-1]}

def p_addFloatType(p):
    '''
    addFloatType : 
    '''
    global memoriaVir, ptype, constTable, current_type, pilaO
    
    # Se genera la direccion virtual apropiada
    memoriaVir, ptype, current_type, pilaO = generaMemoriaConst("floatConst", memoriaVir, "float", ptype, pilaO)
    constTable[pilaO[-1]] = {"Type" : current_type, pilaO[-1] : p[-1]}
     
def p_addCharType(p):
    '''
    addCharType : 
    '''
    global memoriaVir, ptype, constTable, current_type, pilaO

    # Se genera la direccion virtual apropiada
    memoriaVir, ptype, current_type, pilaO = generaMemoriaConst("charConst", memoriaVir, "char", ptype, pilaO)
    constTable[pilaO[-1]] = {"Type" : current_type, pilaO[-1] : p[-1]}
    
def p_addBoolType(p):
    '''
    addBoolType : 
    '''
    global memoriaVir, ptype, constTable, current_type, pilaO

    # Se genera la direccion virtual apropiada
    memoriaVir, ptype, current_type, pilaO = generaMemoriaConst("boolConst", memoriaVir, "bool", ptype, pilaO)
    constTable[pilaO[-1]] = {"Type" : current_type, pilaO[-1] : p[-1]}

# Ingresa el id y el operando a su repectiva fila
def p_push_id(p):
    '''
    push_id : 
    '''   
    global pilaO

    # Se fija si es un arreglo
    if p[-2] != None:  
        # En caso no ser un arreglo se pushea id
        pilaO.append(p[-2])
    # Push =
    pOper.append(p[-1])
    
    
# Puntos para generar el gotmain y actualalizar su salto
# Crea el cuadruplo
def p_gotomain(p):
    '''
    gotomain : 
    '''
    cuad.append(cuadruplos("GOTOMAIN", "", "", 0))

# Actualiza el salto cuando se llama
def p_setmainloc(p):
    '''
    setmainloc : 
    '''
    cuad[0] = (cuadruplos("GOTOMAIN", "", "", len(cuad)))

############################################################
##############           ESTATUTOS        ##################
############################################################

# Escribe
def p_cuadprint(p):
    '''
    cuadprint : 
    '''
    global pilaO, cuad, countCuad 
    # Obtenemos el valor a imprimr
    resultado = pilaO.pop()
    # Generamos el cuadruplo
    aux = cuadruplos("print","","",resultado)
    cuad.append(aux)
    # Incrementamos el contador
    countCuad +=1
    

# Lee
def p_cuadlee(p):
    '''
    cuadlee : 
    '''
    global pilaO, memoriaVir, tempcount, cont, countCuad, current_type, constTable
    # Obtenemos el valor a leer
    resultado = pilaO.pop()
    # Obtenemos la memoria temporal e incrementamos y apunta a la siguiente direccion disponible
    indexVal = returnMemoryType("Temp", constTable[resultado]["Type"])
    result = memoriaVir[indexVal]
    memoriaVir[indexVal] += 1
    # Generamos el cuadruplo
    aux = cuadruplos("lee",resultado,"",result)
    cuad.append(aux)
    # Incrementamos los contadores
    countCuad +=1
    cont += 1
    tempcount += 1

# Retorna
# En caso de tratar de retornar un void genera un error
def p_returnFlag(p):
    '''
    returnFlag : 
    '''
    global current_func, directorio_fun
    if directorio_fun[current_func[-1]]["Type"] == "void":
        catalogoErrores([6, current_func[-1]])

def p_cuadRetornar(p):
    '''
    cuadRetornar : 
    '''
    global pilaO, countCuad
    # Obtenemos el valor a retornar
    resultado = pilaO.pop()
    # Generamos el cuadruplo
    aux = cuadruplos("return","","",resultado)
    cuad.append(aux)
    # Incrementamos los contadores
    countCuad +=1

#######################################################################
##############           CICLOS CONDICIONALES        ##################
#######################################################################

# If, elif, else
# Generamos el cuadruplo GOTOF
def p_genGTF(p):
    '''
    genGTF : 
    '''
    # Generamos el primer cuadruplo para goToF, guardamos su posicion para el jump a futuro
    global pilaO, pjumps, pelse, cont, countCuad
    # Obtenemos el valor booleano para el if
    resultado = pilaO.pop()
    # Generamos el cuadruplo
    cuad.append(cuadruplos("GotoF",resultado,"",0))
    # Apendamos los valores a sus repectivas pilas
    pjumps.append(len(cuad) - 1)
    if (not pelse or pelse[-1] != 'elif') and p[-5] != "while":
        # Si no es else o ifelse se agrega el valor "if" a la pila else
        pelse.append("if")
        saltoselse.append({"if" : len(cuad) - 1})
    # Incrementamos los contadores
    countCuad += 1
    cont += 1

# Generamos el cuadruplo GOTO para else, guardamos su posicion para el jump a futuro
def p_genGT(p):
    '''
    genGT : 
    '''
    global cuad, pjumps, pelse, countCuad
    # Si el token es else generamos el cuadruplo
    if p[-1] == "else":
        # Generar cuadruplo
        cuad.append(cuadruplos("Goto","","",0))
        # Apendamos los valores a sus repectivas pilas
        pjumps.append(len(cuad) - 1)
        # Incrementamos los contadores
        countCuad +=1
    # Apendamos los valores a sus repectivas pilas
    pelse.append(p[-1])  
    saltoselse[-1][p[-1]] = len(cuad) -1


# Ingresa el valor del salto a los goto's generados
def p_fillGoto(p):
    '''
    fillGoto : 
    '''
    global pjumps, cuad, pelse
    if pjumps:
        # Sacamos los valores de las pilas: el salto y GOTO o GOTOF
        end = pjumps.pop()
        resultado = cuad[end].rightop
        # Se les da el valor del jump apropiado, distingue si es goToF o goTo. 
        if cuad[end].op == "GotoF":
            # Si es un else if debe considerar que tiene que dar un salto mas
            if pelse.pop() == "elif":
                cuad[end] = cuadruplos("GotoF",resultado,"",len(cuad))
                ifLoc = saltoselse[-1]['if']
                cuad[ifLoc] = cuadruplos(cuad[ifLoc].op, cuad[ifLoc].rightop, cuad[ifLoc].leftop, cuad[ifLoc].top - 1)
            else:
                if 'elif' in saltoselse[-1].values():
                    ifLoc = saltoselse[-1]['ifelse']
                    cuad[ifLoc] = cuadruplos(cuad[ifLoc].op, cuad[ifLoc].rightop, cuad[ifLoc].leftop, cuad[ifLoc].top - 1)
                cuad[end] = cuadruplos("GotoF",resultado,"",len(cuad) + 1)
        elif cuad[end].op == "Goto" :
            # Genera el cuadruplo GoTo else
            pelse.pop()
            cuad[end] = cuadruplos("Goto",resultado,"",len(cuad)) 
            saltoselse.pop()

# While
def p_storeWhile(p):
    '''
    storeWhile : 
    '''
    global pjumps
    # Punto neuralgico para agregar el valor a la pila de saltos
    pjumps.append(len(cuad) - 1)

# Debemos crear un GoToV para el do while
def p_genDoWhile(p):
    '''
    genDoWhile : 
    '''
    global pjumps, pilaO, cuad, countCuad
    # Obtenemos los valores de su respectivas pilas
    jump = pjumps.pop()
    resultado = pilaO.pop()
    # Creamos el cuadruplo GotoV
    cuad.append(cuadruplos("GotoV",resultado, "",jump + 1))
    # Incrementamos el contador
    countCuad +=1

# Llenamos los valores del gotoV  
def p_fillWhile(p):
    '''
    fillWhile : 
    '''
    global pjumps, cuad, countCuad
    # Obtenemos los valores de su respectivas pilas
    end = pjumps.pop()
    jump = pjumps.pop()
    # Se crea el cuadruplo GoTo (Permanecer en el ciclo)
    cuad.append(cuadruplos("Goto","", "",jump + 1))
    # Se crea el cuadruplo GoToF (Salir del ciclo)
    resultado = cuad[end].rightop
    cuad[end] = cuadruplos("GotoF",resultado,"",len(cuad))
    # Incrementamos el contador
    countCuad +=1

# For
# Punto neuralcico para agregar el id definido en el for loop
def p_addForId(p):
    '''
    addForId : 
    '''
    global pilaO, current_name
    # Agregamos el valor a su pila
    pilaO.append(directorio_fun[current_func[-1]]["Vars"][p[-1]]["Memoria"])
    current_name = p[-1]

#Punto neuralgico para agregar el cuadruplo para controlar el for
def p_genFor(p):
    '''
    genFor : 
    '''
    global current_type, memoriaVir, pOper, countCuad
    # Revisar que el valor sea entero
    if current_type == "int":
        # Obtenemos el valor de su respectiva pila
        exp = pilaO.pop()
        pOper.append(p[-1])
        result, memoriaVir = obtenMemVir(current_func[-1], current_type, memoriaVir, 1)
        # Agregamos a la funcion el vControl
        directorio_fun[current_func[-1]]["Vars"]["vControl"] = newVar(directorio_fun[current_func[-1]]["Vars"], "vControl", current_type, result)
        # crear el cuadruplo de control para el for
        cuad.append(cuadruplos("=",exp,"",result))
        # Incrementamos el contado
        countCuad +=1
    else:
        catalogoErrores([8])

# Punto neuralgico para comprarar la expresion y aggregar el goto en falso
def p_compFor(p):
    '''
    compFor : 
    '''    
    global pilaO, current_type, memoriaVir, current_func, directorio_fun, pjumps, countCuad, cuad, cont
    # Obtenemos el valor de su respectiva pila
    exp = pilaO.pop()
    # Revisar que el valor sea entero
    if current_type == "int":
        # Obtenemos el la direccion virtual: Regresamos el valor y actualizamos la memoria
        result, memoriaVir = obtenMemVir(current_func[-1], current_type, memoriaVir, 1)
        # Se genera vFinal en el directorio de funciones
        directorio_fun[current_func[-1]]["Vars"]["vFinal"] = newVar(directorio_fun[current_func[-1]]["Vars"], "vFinal", current_type, result)
        # Obtenemos el vControl
        vControl = directorio_fun[current_func[-1]]["Vars"]["vControl"]["Memoria"]
        # Generamos temporal
        resultado = memoriaVir["intTemp"]
        memoriaVir["intTemp"] += 1
        # Cuadruplo asignar el resultado de la exprecion a vfinal
        cuad.append(cuadruplos('=',exp,"",result))
        countCuad +=1
        # Cuadruplo comparar vFinal y vControl
        cuad.append(cuadruplos('<',vControl,result,resultado))
        countCuad +=1
        # Agregamos la poscion para el salto
        pjumps.append(len(cuad) - 1)
        # Cuadruplo generar un go to en falso para el final del for
        cuad.append(cuadruplos('GotoF',resultado,"",""))
        countCuad +=1
        # Apendamos los valores e incrementamos el contador
        pjumps.append(len(cuad) - 1)
        cont += 1
    else:
        catalogoErrores([8])

# Punto neuralgico para actualizar el control y actualizar el go en falso anterior  
def p_actFor(p):
    '''
    actFor : 
    '''
    global directorio_fun, current_func, memoriaVir, cuad, countCuad, pjumps, pilaO
    # Obtenemos el vControl
    vControl = directorio_fun[current_func[-1]]["Vars"]["vControl"]["Memoria"]
    resultado = memoriaVir["intTemp"]
    memoriaVir["intTemp"] += 1
    # Cuadruplo sumar 1 al contol
    # Debemos agregar el 1 a la tabla de las constantes
    indexVal = "intConst"
    result = memoriaVir[indexVal]
    memoriaVir[indexVal] += 1
    constTable[result] = {"Type" : "int", result : 1}
    cuad.append(cuadruplos('+',vControl,result,resultado))
    countCuad +=1
    # Cuadruplo asignar el resultado al control
    cuad.append(cuadruplos('=',resultado,"",vControl))
    countCuad +=1
    # Cuadruplo asignar resultado al id original
    cuad.append(cuadruplos('=',resultado,"",pilaO[-1]))
    countCuad +=1
    # Obtenemos donde comienza y a donde va el for 
    fin = pjumps.pop()
    ret = pjumps.pop()
    # Cuadruplo crear go to al inicio
    cuad.append(cuadruplos('Goto',"","",ret))
    countCuad +=1
    # Actualizar el cuadruplo
    resultado = cuad[fin].rightop
    # Cuadruplo actualizar el goto en falso a el cuadruplo donde termina el for
    cuad[fin] = cuadruplos("GotoF",resultado,"",len(cuad))
    pilaO.pop()


###########################################################
##############           FUNCIONES       ##################
###########################################################


#- Definicion de la funcion
# Parametros
def p_newParamType(p):
    '''
    newParamType : 
    '''
    global pParam, current_type
    # Agregamos el tipo de parametro a la tabla 
    pParam.append(current_type)

# Agregamos la tabla de parametros y la cantidad de parametros a su funcion
def p_addParamCount(p):
    '''
    addParamCount : 
    '''
    global directorio_fun, current_func,pParam
    directorio_fun[current_func[-1]]["# Param"] = len(pParam)
    directorio_fun[current_func[-1]]["Param Table"]  = pParam
    pParam = []

# Punto neuralgico para generar el cuadruplo parameter
def p_genParameter(p):
    '''
    genParameter : 
    '''
    global pilaO, ptype, cuad, paramTable
    # Obtener el tipo y valor de sus pilas
    argument = pilaO.pop()
    argumentType = ptype.pop()
    # Si no es el tipo apropiado levanta error
    if argumentType == paramTable[parameterCounter] : 
        # Cuadruplo genera PARAMETER
        parc = "par" + str(parameterCounter) 
        cuad.append(cuadruplos("PARAMETER",argument,parc,""))
    else: 
        catalogoErrores([4, argumentType, paramTable[parameterCounter]])

# Agregamos la cantidad de variables locales y la posicion de cuando comienza la funcion
def p_addContF(p):
    '''
    addContF : 
    '''
    directorio_fun[current_func[-1]]["# VL"] = len(directorio_fun[current_func[-1]]["Vars"])
    directorio_fun[current_func[-1]]["CONT"] = countCuad
    

#- Llamada de la funcion
def p_callFunc(p):
    '''
    callFunc : 
    '''
    global directorio_fun, paramTable, pCurrentCall
    # Verificar que exista la funcion en DirFunciones
    if p[-1] in directorio_fun:
        pCurrentCall.append(p[-1])
        paramTable = directorio_fun[p[-1]]["Param Table"]
        cuad.append(cuadruplos("ERA", "", "", p[-1]))
    else:
        catalogoErrores([11, p[-1]])

# Incrementamos el contador de parametros definidos
def p_paramCounter(p):
    '''
    paramCounter : 
    ''' 
    global parameterCounter
    parameterCounter += 1         

# Al ser el ultimo parametro verificamos que se hayan ingresado la cantidad correcta de parametros, generamos gosub
def p_verLastParam(p):
    '''
    verLastParam : 
    '''
    global pCurrentCall, paramTable, cuad ,cont, pilaO ,parameterCounter, tempcount, directorio_fun, memoriaVir
    if parameterCounter + 1 != len(paramTable):
        catalogoErrores([5])
    else:
        # Cuadruplo gosub
        currentCall = pCurrentCall.pop()
        type = directorio_fun[currentCall]["Type"]
        result1, memoriaVir = obtenMemVir(currentCall, type, memoriaVir, 1)
        cuad.append(cuadruplos("GOSUB", currentCall,"",directorio_fun[currentCall]["CONT"]))
        # Si no es void la funcion 
        if directorio_fun[currentCall]["Type"] != "void":
            type = directorio_fun[currentCall]["Type"]
            memoriaVir, result1, pilaO = generaMemoriaConst(type + "Temp", memoriaVir, type, None, pilaO)
            tempcount += 1
            # Cuadruplo para retornar valor en una funcion no void
            result = directorio_fun[currentCall]["Memoria"]
            ptype.append(directorio_fun[currentCall]["Type"])
            cuad.append(cuadruplos("=",result,"",result1 - 1))
            parameterCounter = 0
            cont += 1
        paramTable = []

##########################################################
##############           ARREGLOS       ##################
##########################################################

# Definicion de arreglos
# Vamos a agregar el li o ls
def p_setL(p):
    '''
    setL : 
    '''
    global r,current_func,current_name, dim, directorio_fun
    node = directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][dim]
    # Si no existe se agrega li nodo, si ya existe significa que ya tiene li entonces agrega ls y calcula r
    if node:
        r = (int(p[-1]) - int(node[0]) + 1) * r       
    directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][dim].append(p[-1])

# Si es un array se marca en el directorio de funciones y inicializa el primer nodo en dim
def p_newArray(p):
    '''
    newArray : 
    '''
    global current_func, directorio_fun, current_name, dim, r
    #inicializar dim y r en 1 
    dim = 1
    r = 1
    # Al ser nuevo arreglo lo declaramos y creamos una lista de nodos vacia
    directorio_fun[current_func[-1]]["Vars"][current_name]["isArray"] = True
    directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"] = {dim : []}

def p_cerrarNodes(p):
    '''
    cerrarNodes :
    '''
    global current_func, directorio_fun, current_name, dim, r, k
    # Volvemos a declarar las variables a utlizar
    dim = 1
    offset = 0
    size = r
    lenNodes = len(directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"])
    for node in directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"]:
        # Obtenemos los valores en la dimension correcta
        nodeval = directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][node]
        ls = int(nodeval[1])
        li = int(nodeval[0])
        # Calculamos los valores para el offset
        m = r / (ls - li + 1)
        r = m
        offset = offset + li * m
        # Mientras que haya otro nodo el la lista apendamos m, si no (-k)
        if lenNodes != dim:
            directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][node].append(m)
        else:
            k = offset
            indexVal = "intConst"
            result = memoriaVir[indexVal]
            memoriaVir[indexVal] += 1
            constTable[result] = {"Type" : "int", result : k}
            directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][node].append(k * -1)
        dim += 1
    # Generamos la memoria apropiada (size)
    memoryIndex = returnMemoryType(current_func[-1], current_type)
    memoriaVir[memoryIndex] += size

# Creamos el cuadruplo para la verficacion
def p_crearCuadA(p):
    '''
    crearCuadA : 
    '''
    global dimNode, cuad, tempcount, pilaO, pilaDim, memoriaVir, directorio_fun, current_name,arraux
    # Obtenemos el numero que se le ingreso al arreglo
    resultado = pilaO[-1]
    # Cuadruplo verify.
    cuad.append(cuadruplos("VERIFY",resultado ,dimNode[0], dimNode[1]))
    # Si tiene otro nodo por seguir
    current_name = arraux
    if (pilaDim[-1] + 1) in directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"]:
        # Se obtienen las dimensiones y se multiplican para actualizar el offset
        aux = pilaO.pop()
        m = directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][pilaDim[-1]][2]
        result, memoriaVir = obtenMemVir("Temp", current_type, memoriaVir, 1)
        tempcount += 1
        # Ingresamos m a la memoria
        memoriaVir, ptype, current_type, pilaO = generaMemoriaConst("intConst", memoriaVir, "int", ptype, pilaO)
        constTable[pilaO[-1]] = {"Type" : current_type, pilaO[-1] :int(m)}
        ptype.pop()
        cuad.append(cuadruplos('*',aux,int(m),result))
        pilaO.append(directorio_fun[current_func[-1]]["Vars"][current_name]['Memoria'])
    if pilaDim[-1] > 1:
        # Se va haciendo la sumatoria de los calculos del offset
        auxAddress = memoriaVir[returnMemoryType("Temp", current_type)] - 1
        aux2 = pilaO.pop()
        pilaO.pop()
        result, memoriaVir = obtenMemVir("Temp", current_type, memoriaVir, 1)      
        tempcount += 1
        cuad.append(cuadruplos('+',aux2, auxAddress,result))
        pilaO.append(result)
    

def p_crearCuadB(p):
    '''
    crearCuadB : 
    '''
    global pilaO, cuad, k
    # Generamos la memoria virtual para los cuadruplos de matrices
    aux = pilaO.pop()
    indexVal = returnMemoryType("Temp", current_type)
    temp1 = memoriaVir[indexVal]
    memoriaVir[indexVal] += 1
    # Agregamos el cudadruplo para la suma del offset, si se manda una variable obtenemos la posicion en memoria 
    cuad.append(cuadruplos('+', int(k), aux, temp1))
    # Generamos memoria para el temporal
    temp2 = memoriaVir[indexVal]
    memoriaVir[indexVal] += 1
    # Agregamos el cuadruplo 
    virtualAddress = directorio_fun[current_func[-1]]["Vars"][current_name]["Memoria"]
    cuad.append(cuadruplos('+', temp1, virtualAddress, temp2))

def p_agregarVar(p):
    '''
    agregarVar :
    '''
    global current_func, directorio_fun, current_name,arraux
    # Agregamos la direccion virtual y su tipo a la pila
    if(p[-1] == '['):
        arraux = p[-2]

    current_name = p[-2]
    pilaO.append(directorio_fun[current_func[-1]]["Vars"][p[-2]]["Memoria"])
    ptype.append(directorio_fun[current_func[-1]]["Vars"][current_name]["Type"])

# Verificamos que se este llamando a un arreglo
def p_verifyAEx(p):
    '''
    verifyAEx :
    '''
    global pilaO, ptype, directorio_fun, dimNode, current_name, current_type, pilaDim
    # Sacamos los valores de sus respectivas filas
    current_type = ptype.pop()
    pilaO.pop()
    # Si es un array se genera la dimension y apunta al primer nodo, si no levanta un error
    try:
        if directorio_fun[current_func[-1]]["Vars"][current_name]["isArray"]:
            dim = 1
            pilaDim.append(dim)
            dimNode = directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][dim]
        else:
            catalogoErrores([10, current_name])
    except:
        catalogoErrores([10, current_name])

# Se actualiza el nodo al que le apuntamos en la dimension
def p_updateDim(p):
    '''
    updateDim  :
    '''
    global dim, dimNode, pilaDim, current_name
    # Incrementamos dim, actualizamos la pila dim y mandamos llamar a su repespectivo nodo
    pilaDim[-1] = pilaDim[-1] + 1
    dimNode = directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][pilaDim[-1]]

# En caso de tener mas de una dimension se incrementa
def p_increaseDim(p):
    '''
    increaseDim :
    '''
    global directorio_fun, current_name, dim
    dim += 1
    directorio_fun[current_func[-1]]["Vars"][current_name]["Nodes"][dim] = []

yacc.yacc()

def runLexerParser(fileTxt, filename, valoresMemoria):
    global memoriaVir, memoriaTemp
    # Vamos a definir las direcciones iniciales para la memoria virtual
    # Para cada modulo de memoria se definen los tipos
    particionesDeMemoria = ["intConst", "floatConst", "charConst", "boolConst",
                            "intLocal", "floatLocal", "charLocal", "boolLocal",
                            "intGlobal", "floatGlobal", "charGlobal", "boolGlobal",
                            "intTemp", "floatTemp", "charTemp", "boolTemp"]

    # Hacemos la llamada para generar memoria
    memoria = generaMemoria(valoresMemoria)

    # Guardamos las dirreciones dentro de un diccionario
    memoriaVir = dict(zip(particionesDeMemoria, memoria))

    # Guardamos los valores de los temporales para reiniciar la memoria cuando se deba
    memoriaTemp = dict(zip(particionesDeMemoria[4:8], memoria[4:8]))


    
    yacc.parse(fileTxt)
    # logger
    editPrintLogger("Compilacion exitosa!")

    return obj
 
