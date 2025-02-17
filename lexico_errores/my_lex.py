import lexico_errores.lexical as lexical
import lexico_errores.err as err
from tabulate import tabulate
 

#file = "test/008_errors.txt"

def lex_analyze(src_file):
    tokens,errores_lexicos = lexical.lexical_analysis(src_file)
    #headers = ['Token', 'Type', 'Row', 'Column']
    tokens = [token for token in tokens if "comment" not in token[1]]

    errores = None

    #print(tabulate(tokens, headers=headers, tablefmt="grid"))
    if errores_lexicos:
        errores = err.process_errors(errores_lexicos)
        for detail in errores:
            print(f"Mensaje: {detail['message'] }    Línea :{detail['line']} ")
        return tokens, errores

    return tokens, errores
    


#main()