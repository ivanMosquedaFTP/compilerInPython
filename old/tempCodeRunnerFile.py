#######################################################################
###############         ANALISIS        ###############################
#######################################################################

# Clase Token
class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type  # Tipo de token (ej. identificador, número, etc.)
        self.value = value      # Valor del token (ej. nombre del identificador o literal numérico)
        self.line = line        # Número de línea donde se encontró el token
        self.column = column    # Posición del token en la línea

    def __repr__(self):
        return f"Token(type={self.type}, value='{self.value}', line={self.line}, column={self.column})"


# Clase LexicalAnalyzer
class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code.splitlines()  # Código fuente dividido por líneas
        self.line_number = 0                         # Número de línea actual
        self.column_number = 0                       # Posición actual en la línea
        self.current_line = self.source_code[self.line_number] if self.source_code else ""
        self.reserved_words = {"if", "else", "while", "for", "return"}  # Palabras reservadas del lenguaje

    def next_token(self):
        # Lógica para leer el siguiente token en el código fuente
        # Aquí puedes agregar la lógica detallada para escanear caracteres y formar tokens
        pass

    def is_valid_identifier(self, string):
        # Verifica si la cadena cumple las reglas para un identificador
        return string.isidentifier()

    def is_reserved_word(self, string):
        # Verifica si la cadena es una palabra reservada del lenguaje
        return string in self.reserved_words

    def get_next_char(self):
        # Método auxiliar para obtener el siguiente carácter del código fuente
        if self.column_number < len(self.current_line):
            char = self.current_line[self.column_number]
            self.column_number += 1
            return char
        else:
            # Fin de línea alcanzado
            self.line_number += 1
            if self.line_number < len(self.source_code):
                self.current_line = self.source_code[self.line_number]
                self.column_number = 0
                return self.get_next_char()
            else:
                return None  # Fin del código fuente


# Clase SymbolTable
class SymbolTable:
    def __init__(self):
        self.table = {}  # Estructura de almacenamiento para la tabla de símbolos, se puede utilizar un diccionario

    def insert(self, symbol, symbol_type, scope):
        # Inserta un nuevo símbolo en la tabla
        if scope not in self.table:
            self.table[scope] = {}
        self.table[scope][symbol] = {'type': symbol_type, 'scope': scope}

    def lookup(self, symbol, scope):
        # Busca un símbolo en el ámbito dado
        return self.table.get(scope, {}).get(symbol, None)

    def update(self, symbol, symbol_type, scope):
        # Actualiza el tipo de un símbolo existente en el ámbito dado
        if scope in self.table and symbol in self.table[scope]:
            self.table[scope][symbol]['type'] = symbol_type

    def __repr__(self):
        return f"SymbolTable({self.table})"

