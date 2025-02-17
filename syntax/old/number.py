import sys

class Numero:
    def __init__(self,valor):
        self.valor = valor
        self.set_position()

    def __repr__(self):
        return f'{self.valor}'

    def set_position(self, row_pos=None,col_pos=None):
        self.row_pos = row_pos
        self.col_pos = col_pos
        return self  
    
    def suma(self, otro):
        t1 = self.processnumber(self)
        t2 = self.processnumber(otro)
        if isinstance(self, Numero):
            return Numero(t1  + t2)

    def resta(self, otro):
        t1 = self.processnumber(self)
        t2 = self.processnumber(otro)
        if isinstance(self, Numero):            
            return Numero(t1 - t2)

    def multiplicacion(self, otro):
        t1 = self.processnumber(self)
        t2 = self.processnumber(otro)
        if isinstance(self, Numero):
            return Numero(t1 * t2)
 

    def division(self, otro):
        t1 = self.processnumber(self)
        t2 = self.processnumber(otro)
        if t2 == 0:
            return  "div 0"
        if isinstance(self, Numero):
            return Numero(t1 / t2)
            

    

    def get_comparacion_igual(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 == t2))


    def get_comparacion_diferente(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 != t2))

    def get_comparacion_menor(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 < t2))
 
    def get_comparacion_mayor(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 > t2))

    def get_comparacion_menor_igual(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 <= t2))

    def get_comparacion_mayor_igual(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 >= t2))

    def get_and(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 and t2))

    def get_or(self, other):
        t1 = self.processnumber(self)
        t2 = self.processnumber(other)
        if isinstance(other, Numero):
            return Numero(int(t1 or t2))
        

    def processnumber(self,number):
        if isinstance(number.valor,int):
            return number.valor
        if isinstance(number.valor,float):
            return int(number.valor)
        return int(number.valor.token[0])