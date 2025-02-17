from syntax.node import NodoNumero,NodoOperacion,NodoNegativo,NodoAsignacion
from syntax.three_results import ResultsThree

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
        self.errors = []
        self.asign = []
        

    def advance(self):
        self.token_index +=1
        if self.token_index< len(self.tokens) :
            self.current_token = self.tokens[self.token_index]
        return self.current_token
    

    def parse(self):
        res = self.expresion()
        #not self.errors
        if self.errors and self.current_token[1] != "end":
            self.errors.append({"code": "se esperaba un operador aritmetico", "line": self.current_token[2], "col": self.current_token[3], "place":"-s"})
        return res,self.errors
    
    def factor(self):
        resultado = ResultsThree()
        token = self.current_token

        if token[1] == "minus":
            resultado.registro(self.advance()) 
            factor = resultado.registro(self.factor())
            if self.errors:
                return resultado
            return resultado.exito(NodoNegativo(token,factor))

        if token[1] == "number":
            resultado.registro(self.advance()) 
            return resultado.exito(NodoNumero(token))
        
        if token[1] == "paren_l":
            resultado.registro(self.advance()) 
            expr = resultado.registro(self.expresion())
            if self.errors: 
                return resultado
            token = self.current_token
            if token[1] == "paren_r":
                resultado.registro(self.advance())
                return resultado.exito(expr)
            else:
                self.errors.append({"code": "Se esperaba un )", "line": self.current_token[2], "col": self.current_token[3], "place":"-s"})
                return resultado
        self.errors.append({"code": "Se esperaba un entero", "line": self.current_token[2], "col": self.current_token[3], "place":"-s"})
        return resultado       

          
    def term(self):
        return self.operacion_algebraica(self.factor,("times","divide"))
    
    def expresion_aritmetica(self):
        return self.operacion_algebraica(self.term,("plus","minus"))
    
    def expresion(self):
        nodo = self.operacion_algebraica(self.comparacion,("or","and"))
        if self.errors:
             self.errors.append({"code": "se esperaba un '-' o un '('", "line": self.current_token[2], "col": self.current_token[3], "place":"-s"})
        return nodo
    
    def comparacion(self):
        nodo = self.operacion_algebraica(self.expresion_aritmetica, ("mayor","menor","igual","mayor_igual","menor_igual","diferente"))
        if self.errors:
            self.errors.append({"code": "se esperaba un int, identificador, '-', '(' ", "line": self.current_token[2], "col": self.current_token[3], "place":"-s"})
        return nodo

    def operacion_algebraica(self, funcion, operadores):
        resultado = ResultsThree()
        izquierdo = resultado.registro(funcion())
        if self.errors:
            return resultado
        while self.current_token[1] in operadores:
            operador = self.current_token
            resultado.registro(self.advance())
            derecho = resultado.registro(funcion())
            izquierdo = NodoOperacion(izquierdo,operador,derecho)
        return resultado.exito(izquierdo)

    def asignacion(self):
        resultado = ResultsThree()

        # Se espera la palabra clave `int`
        if self.current_token[1] == "int":
            tipo = self.current_token[0]  # Guardamos el tipo, en este caso 'int'
            resultado.registro(self.advance())

            # Procesamos la regla <asignacion_detalle>
            asignacion_detalle = resultado.registro(self.asignacion_detalle(tipo))
            if self.errors:
                return resultado

            # Confirmamos que termine con ';'
            if self.current_token[1] == "semicolon":
                resultado.registro(self.advance())
                return resultado.exito(asignacion_detalle)
            else:
                self.errors.append({
                    "code": "Se esperaba ';'",
                    "line": self.current_token[2],
                    "col": self.current_token[3],
                    "place": "-s"
                })
                return resultado

        # Si no empieza con `int`, es un error
        self.errors.append({
            "code": "Se esperaba 'int'",
            "line": self.current_token[2],
            "col": self.current_token[3],
            "place": "-s"
        })
        return resultado
    

    def asignacion_detalle(self, tipo):
        resultado = ResultsThree()
        token = self.current_token

        # Caso: id = expr
        if token[1] == "id":
            self.advance()

            # Si hay un igual, se espera una expresión
            if self.current_token[1] == "asign":
                self.advance()
                expr = resultado.registro(self.expresion())
                if self.errors:
                    return resultado
                nodo_asignacion = NodoAsignacion(tipo, token, expr)

                # Si hay más asignaciones separadas por coma
                if self.current_token[1] == "comma":
                    self.advance()
                    siguiente_detalle = resultado.registro(self.asignacion_detalle(tipo))
                    if self.errors:
                        return resultado

                    # Fusionamos los detalles en un nodo único
                    nodo_asignacion.siguiente = siguiente_detalle
                    return resultado.exito(nodo_asignacion)

                # Retorno simple si no hay más detalles
                return resultado.exito(nodo_asignacion)

            # Caso: solo `id` sin asignación
            nodo_asignacion = NodoAsignacion(tipo, token)
            if self.current_token[1] == "comma":
                self.advance()
                siguiente_detalle = resultado.registro(self.asignacion_detalle(tipo))
                if self.errors:
                    return resultado

                nodo_asignacion.siguiente = siguiente_detalle
            return resultado.exito(nodo_asignacion)

        self.errors.append({
            "code": "Se esperaba un identificador después del tipo.",
            "line": self.current_token[2],
            "col": self.current_token[3],
            "place": "-s"
        })
        return resultado
    

"""
            if self.current_token[1] == "id":
                self.advance()
                name = self.current_token
                if self.current_token[1] == "asign":
                    self.advance()
                    expr = self.expresion()
                
                if self.current_token[1] == "comma":
                    self.advance()
                    self.asign.append("")
                    expr = self.expresion()
                    if self.errors:
                        return expr
                    NodoVariable(name, expr)
                    """