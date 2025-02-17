from syntax.number import Numero
from syntax.symbolTable import SymbolTable
import sys
class Executer:
    def __init__(self):
        self.executer_errors = []
        self.symboltable = SymbolTable()

    def operation(self,nodo):
        operacion =  type(nodo).__name__
        ejecutar = getattr(self,operacion,self.fracaso)
        return ejecutar(nodo)
    
    def fracaso(self,nodo):
        raise Exception("mala suerte chap")
    
    def NodoNumero(self,nodo):
        return Numero(nodo).set_position(nodo.row_pos,nodo.col_pos)

    def NodoOperacion(self,nodo):
        izquierda = self.operation(nodo.nodo_izquierdo)
        if self.executer_errors:
            return izquierda
        derecho =  self.operation(nodo.nodo_derecho)
        if self.executer_errors:
            return derecho

        if nodo.operador[1] == "plus":
            resultado = izquierda.suma(derecho)
        elif nodo.operador[1] == "minus":
            resultado = izquierda.resta(derecho)
        elif nodo.operador[1] == "times":
            resultado = izquierda.multiplicacion(derecho)
        elif nodo.operador[1] == "divide":
            resultado = izquierda.division(derecho) 
        elif nodo.operador[1] == "mayor":
            resultado = izquierda.get_comparacion_mayor(derecho)
        elif nodo.operador[1] == "menor":
            resultado = izquierda.get_comparacion_menor(derecho)
        elif nodo.operador[1] == "igual":
            resultado = izquierda.get_comparacion_igual(derecho)
        elif nodo.operador[1] == "mayor_igual":
            resultado = izquierda.get_comparacion_mayor_igual(derecho)
        elif nodo.operador[1] == "menor_igual":
            resultado = izquierda.get_comparacion_menor_igual(derecho)
        elif nodo.operador[1] == "diferente":
            resultado = izquierda.get_comparacion_diferente(derecho)
        elif nodo.operador[1] == "and":
            resultado = izquierda.get_and(derecho)
        elif nodo.operador[1] == "or":
            resultado = izquierda.get_or(derecho)

        if resultado == "div 0":
            self.executer_errors.append({"code": "No se puede dividir entre 0", "line": nodo.operador[2], "col": nodo.operador[3], "place":"-sem"})
            return izquierda
        return resultado.set_position(nodo,nodo)

    def NodoNegativo(self,nodo):
        numero = self.operation(nodo.nodo)
        if self.executer_errors:
            return numero

        if nodo.operador[1] == "minus":
            numero = numero.multiplicacion(Numero(-1))
        return numero.set_position(nodo.row_pos,nodo.col_pos)
    

    def NodoAcceso(self, nodo):
        nombre = nodo.nombre
        valor = self.symboltable.get(nombre)

        if not valor:
            self.executer_errors.append({"code":f'{nombre}'+ " no esta definido", 
                                         "line": nodo.pos_start, 
                                         "col": nodo.col_pos, 
                                         "place":"-sem"})
        return valor
    
    def NodoAsignacion(self, nodo):
        nombre = nodo.nombre
        tipo = nodo.type
        if "Nodo" in nodo.valor.__class__.__name__:
            valor = self.operation(nodo.valor)
        else:
            valor = nodo.valor

        self.symboltable.set(tipo,nombre,valor)

