class NodoNumero:
    def __init__(self,token):
        self.token = token
        self.row_pos = self.token[2]  
        self.col_pos = self.token[3]  


    def __repr__(self):
        return f'{self.token[0]}'
    
class NodoOperacion: 
    def __init__(self,nodo_izquierdo, operador, nodo_derecho):
        self.nodo_izquierdo = nodo_izquierdo
        self.operador = operador
        self.nodo_derecho =nodo_derecho
        self.row_pos = self.operador[2]  
        self.col_pos = self.operador[3]  
    
    def __repr__(self):
        return f'({self.nodo_izquierdo} {self.operador[0]} {self.nodo_derecho})'
    
class NodoNegativo:
    def __init__(self,operador, nodo):
        self.operador = operador
        self.nodo = nodo
        self.row_pos = self.operador[2]
        self.col_pos = self.operador[3]
        
    def __repr__(self):
        return f'{self.operador[0]} {self.nodo}'

class NodoAcceso:
    def __init__(self, nombre):
        self.nombre = nombre[0]
        self.pos_start = nombre[2]
        self.col_pos = nombre[3]

class NodoAsignacion:
    def __init__ (self, type,token, nodo_valor=None):
        self.nombre = token[0]
        self.type = type
        if nodo_valor:
            self.valor = nodo_valor
        else:
            if type == "int":
                self.valor =  0
            elif type == "string":
                self.valor =  ""
            elif type == "boolean":
                self.valor =  False
        self.row_pos = token[2]
        self.col_pos = token[3]

    def __repr__(self):
        return f'type = {self.type},{self.nombre} = {self.valor}'
    
class NodoSi:
     def __init__ (self, cases,else_cases):
        self.cases = cases
        self.else_cases = else_cases

class NodoImpresion:
    def __init__ (self,valor ):
        self.valor = valor
        print (valor)