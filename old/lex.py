# Definir los tipos de caracteres para las columnas de la matriz
CHAR_TYPES = {
    'letter': 0,
    'digit': 1,
    'dot': 2,
    'operator': 3,
    'delimiter': 4,
    'whitespace': 5,
    'quote': 6,
    'other': 7
}

result = []

# Matriz de transición extendida
transition_matrix = [
    # letter  digit  dot   operator delimiter whitespace quote other
    [ 1,      2,     -1,   4,       6,        0,        5,    -1 ],  # Estado 0: Inicial
    [ 1,      1,     -1,   -2,      -2,       -2,       -1,   -2 ],  # Estado 1: Identificador
    [ -2,     2,     3,    -2,      -2,       -2,       -1,   -2 ],  # Estado 2: Entero
    [ -1,     3,     -1,   -2,      -2,       -2,       -1,   -2 ],  # Estado 3: Flotante
    [ -2,     -2,    -2,   4,       -2,       -2,       -2,   -2 ],  # Estado 4: Operador
    [ 5,      5,     5,    5,       5,        5,        -2,   5  ],  # Estado 5: Literal de cadena
    [ -2,     -2,    -2,   -2,      -2,       -2,       -2,   -2 ],  # Estado 6: Delimitador
]

# Diccionario de palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'print': 'PRINT',
    'read': 'READ',
}

# Función para identificar el tipo de carácter
def char_type(char):
    if char.isalpha():
        return CHAR_TYPES['letter']
    elif char.isdigit():
        return CHAR_TYPES['digit']
    elif char == '.':
        return CHAR_TYPES['dot']
    elif char in "+-*/=<>!":
        return CHAR_TYPES['operator']
    elif char in "();{}[],.":
        return CHAR_TYPES['delimiter']
    elif char in " \t\n":
        return CHAR_TYPES['whitespace']
    elif char == '"':
        return CHAR_TYPES['quote']
    else:
        return CHAR_TYPES['other']

# Análisis léxico usando la matriz de transición extendida
def lexer(src_code):
    state = 0
    tokens = []
    current_token = ""
    i = 0
    inside_string = False  # Bandera para saber si estamos dentro de una cadena literal

    while i < len(src_code):
        char = src_code[i]
        col = char_type(char)

        """
        
        """
        # Si estamos dentro de una cadena, acumulamos todo en el token hasta encontrar otra comilla
        if inside_string:
            if col == CHAR_TYPES['quote']:  # Cerrar la cadena literal
                tokens.append((current_token, 'STRING_LITERAL'))
                current_token = ""
                inside_string = False
                state = 0
            else:  # Continuar acumulando caracteres de la cadena
                current_token += char
            i += 1
            continue

        next_state = transition_matrix[state][col]

        if next_state == -1:
            print(f"Error léxico en carácter '{char}' en posición {i}")
            i += 1
            state = 0
            current_token = ""
        elif next_state == -2:
            if current_token:
                token_type = reserved.get(current_token, 'IDENTIFIER' if state == 1 else 'INT_LITERAL' if state == 2 else 'FLOAT_LITERAL' if state == 3 else 'OPERATOR' if state == 4 else 'DELIMITER')
                tokens.append((current_token, token_type))
            current_token = ""
            state = 0
        elif col == CHAR_TYPES['quote']:
            # Al encontrar una comilla, iniciar una cadena literal si no estamos dentro de otra
            inside_string = True
            current_token = ""  # Limpiar el token para empezar a acumular la cadena
            state = 5  # Cambiar al estado de cadena literal
            i += 1  # Mover el índice para evitar incluir la comilla en la cadena
            continue
        else:
            state = next_state
            if col != CHAR_TYPES['whitespace']:
                current_token += char
            i += 1

    # Último token al final del archivo
    if current_token and not inside_string:
        token_type = reserved.get(current_token, 'IDENTIFIER' if state == 1 else 'INT_LITERAL' if state == 2 else 'FLOAT_LITERAL' if state == 3 else 'OPERATOR' if state == 4 else 'DELIMITER')
        tokens.append((current_token, token_type))

    return tokens

# Código de ejemplo para analizar
src_code = '''
int x = 10;
float y = 3.14;
string name = "Juan";
if (x < y) {
    print("x es menor que y");
} else {
    print("x es mayor o igual que y");
}
boolean flag = true;
while (flag) {
    x = x + 1;
    if (x > 20) {
        flag = false;
    }
}
'''

# Ejecutar el análisis léxico
tokens = lexer(src_code)
for token in tokens:
    print(token)