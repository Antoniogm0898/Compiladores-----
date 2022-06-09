import pandas as pd
from Managers.errManager import catalogoErrores

def newTV():
    varTable = {
    }
    return varTable

def newVar(existing_df, idVal, idType,memoria):

    if idVal in existing_df:
        catalogoErrores([0, str(idVal)])
    else:
        newLine = {"Type" : idType,"Memoria" : memoria}
            
    return newLine

# Creacion de cuadruplos

class cuadruplos : 
    def __init__(self,op, rightop, leftop,top):
        self.op = op
        self.rightop = rightop
        self.leftop = leftop
        self.top = top


#####################################################################
##############             CUBO SEMANTICO            ################
#####################################################################

# La funcion aplica y retorna el resultado del cubo semantico
def apply_cubo_semantico(left_oper,right_oper,operator):
    try:
        return cubo_semantico[left_oper][right_oper][operator]
    except:
        return cubo_semantico[right_oper][left_oper][operator]

# Vamos a crear el cubo semantico para los tipos
cubo_semantico = {
   'int':{ 
        'int':{ # Int - Int
            # Suma, resta, mod, mult : int
            '+' : 'int', '-' : 'int', '%' : 'int', '*' : 'int',
            # Div : float
            '/' : 'float',
            # GT, LT, EQ, NOT EQ, EGT, ELT : bool
            '<' : 'bool', '>' : 'bool', '!=' : 'bool', '==' : 'bool', '<=' : 'bool', '>=' : 'bool',
            # AND, OR : error
            '&&': 'err', '||' : 'err',
            # Assignment : True (Si corresponde el tipo de variable con el valor)
            '=' : True            
        },
        'float':{ # Int - Float
            # Mod : int
            '%' : 'int',
            # Suma, resta, multi, div : float
            '+' : 'float', '-' : 'float', '/' : 'float', '*' : 'float',
            # GT, LT, AND, OR, EQ, NOT EQ, EGT, ELT : bool
            '<' : 'bool', '>' : 'bool', '!=' : 'bool', '==' : 'bool', '<=' : 'bool', '>=' : 'bool',
            # AND, OR : error
            '&&' : 'err', '||' : 'err',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=' : False
        },
        'bool':{ # Int - Bool
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, EQ, NOT EQ, EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            # AND, OR : bool
            '!=' : 'bool', '==' : 'bool',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=': False

        },
        'char':{ # Int - Char
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, EQ, NOT EQ, EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            # AND, OR : bool
            '!=' : 'bool', '==' : 'bool',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=': False
        }
    },
    'float':{
        'float':{ # Float - Float
            # Suma, resta, multi, div : float
            '+' : 'float', '-' : 'float', '/' : 'float', '*' : 'float',
            # Mod : int
            '%' : 'int',
            # GT, LT, AND, OR, EQ, NOT EQ, EGT, ELT : bool
            '<' : 'bool', '>' : 'bool', '!=' : 'bool', '==' : 'bool', '<=' : 'bool', '>=' : 'bool',
            # AND, OR : error
            '&&' : 'err', '||' : 'err',
            # Assignment : True (Si corresponde el tipo de variable con el valor)
            '=' : True
        },
        'bool':{ # Float - Bool
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            #  EQ, NOT EQ : err
            '!=' : 'err', '==' : 'bool',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=': False
        },
        'char':{ # Float - Char
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            # EQ, NOT EQ : bool
            '!=' : 'err', '==' : 'err',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=': False
        }
    },
    'bool':{
        'bool':{
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, , EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '<=' : 'err', '>=' : 'err',
            # AND, OR, EQ, NOT EQ : bool
            '!=' : 'bool', '==' : 'bool', '&&' : 'bool', '||' : 'bool',
            # Assignment : True (Si corresponde el tipo de variable con el valor)
            '=': True
        },
        'char':{
            # Suma, resta, div, mult, mod, GT, LT, AND, OR, EGT, ELT : error
            '+' : 'err', '-' : 'err', '/' : 'err', '*' : 'err', '%' : 'err', '<' : 'err', '>' : 'err',
            '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            # EQ, NOT EQ : bool
            '!=' : 'bool', '==' : 'bool',
            # Assignment : False (Si corresponde el tipo de variable con el valor)
            '=': False
        }
    },
    'char':{
        'char':{
            # Suma, resta, div, mul : char
            '+' : 'char', '-' : 'char', '/' : 'err', '*' : 'char',
            # Mod, GT, LT, AND, OR, EGT, ELT
            '%' : 'err', '<' : 'err', '>' : 'err', '&&' : 'err', '||' : 'err', '<=' : 'err', '>=' : 'err',
            # EQ, NOT EQ, GTE
            '!=' : 'bool',
            '==' : 'bool',
            '=' : True
        }
    }
}
