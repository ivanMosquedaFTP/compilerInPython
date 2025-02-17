class SymbolTable:
    def __init__(self):
        self.symbol = {}
    
    def set(self,type, name, value):
        self.symbol[name] = {"type": type, "value": value}

    def get(self,name):
        valor = self.symbol.get(name,None)
        return valor
    
    def remove(self, name):
        del self.symbol[name]
        