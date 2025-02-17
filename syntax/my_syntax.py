from syntax.parser_1 import Parser  
#from syntax.executer import Executer
 
#file = "test/010_goodboy.txt"

def my_syntax(tokens):
        
    ################################################################3
    parser = Parser(tokens)
    
    res = None
    three = None 
    syntax_errors = None
    errores_semantico = None

    #Obtener el árbol
    three,syntax_errors = parser.parse()
    #print("RESULTADO PARSER: "+ str(three))
    message = None
    if syntax_errors:
        #print (syntax_errors)
        for error in syntax_errors:
            message = (
            f"Error: {error['code']} en la Línea: {error['line']}, Columna: {error['col']}."
        )
        return three, message, parser

    ################################################################3
    """
    else:
        executer = Executer()
        #print("RESULTADO EXECUTER: "+ str(three))
        #print("RESULTADO FINAL "+ str(executer.operation(three.nodo)))
        res = executer.operation(three.nodo)
        errores_semantico = executer.executer_errors
        for name, symbol in executer.symboltable.symbol.items():
            print(f"Variable: {name}, Type: {symbol['type']}, Value: {symbol['value']}")

        print(errores_semantico)
    """
    

    return three, message, parser


