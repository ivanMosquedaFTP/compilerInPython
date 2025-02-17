class ResultsThree:
    def __init__(self):
        self.nodo = None

    def __repr__(self):
        return f'{self.nodo}'

    def registro (self, resultado):
        if isinstance (resultado, ResultsThree):
            return resultado.nodo
        return resultado
    
    def exito (self, nodo):
        self.nodo = nodo
        return self
    
