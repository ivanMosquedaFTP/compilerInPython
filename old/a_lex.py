import ply.lex as lex

# Lista de tokens
tokens = [
    # Identificadores y palabras reservadas
    'IDENTIFIER',
    'INT_LITERAL',
    'STRING_LITERAL',

    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR', 'NOT',
    'ASSIGN',
    'INCREMENT', 'DECREMENT',

    # Delimitadores
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET', 'SEMICOLON', 'DOT',

    # Comentarios (manejo especial en `t_ignore`)
]

# Palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'int': 'INT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'print': 'PRINT',
    'read': 'READ',
}

# Agrega las palabras reservadas a la lista de tokens
tokens += list(reserved.values())

# Reglas de expresiones regulares para tokens de caracteres individuales
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
t_DIVIDE      = r'/'
t_EQ          = r'=='
t_NEQ         = r'!='
t_LT          = r'<'
t_GT          = r'>'
t_LE          = r'<='
t_GE          = r'>='
t_AND         = r'&&'
t_OR          = r'\|\|'
t_NOT         = r'!'
t_ASSIGN      = r'='
t_INCREMENT   = r'\+\+'
t_DECREMENT   = r'--'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_SEMICOLON   = r';'
t_DOT   = r'\.'

# Literales
t_ignore = ' \t'  # Ignorar espacios y tabulaciones

# Definiciones de token adicionales
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verificar si es palabra reservada
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)
    return t

# Comentarios
def t_COMMENT_LINE(t):
    r'//.*'
    pass  # Ignorar comentarios de línea

def t_COMMENT_BLOCK(t):
    r'/\*[^*]*\*/'
    pass  # Ignorar comentarios de bloque

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores léxicos
def t_error(t):
    print(f"Caracter no reconocido '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

def analyze(src):
    lexer.input(src)
    tokens = []
    lexer.lineno = 1
    for tok in lexer:
        col = tok.lexpos - src.rfind('\n',0,tok.lexpos)
        tokens.append((tok.value, tok.type, tok.lineno, col))
    return tokens 


if __name__ == '__main__':
    src_code = """
    int x = 5
    float y = 10.2
    string a = "Hola"
    print(a)

    """
    #print(analyze(src_code))
    tokens = analyze(src_code)
    for t in tokens:
        print(t)
        print("")
