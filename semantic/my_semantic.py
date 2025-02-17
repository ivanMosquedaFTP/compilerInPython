from semantic.executer import Executer


def my_semantic(three,parser):

    executer = Executer()
    #print("RESULTADO EXECUTER: "+ str(three))
    #print("RESULTADO FINAL "+ str(executer.operation(three.nodo)))
    #res = executer.operation(three.nodo)
    message = None
    #errores_semantico = executer.executer_errors
    outs_list = []
    outs = None
    """
    if errores_semantico:
        message = errores_semantico
        print(message)
    """
    print (parser.result)
    index = 0 
    for node in parser.result:
        ( executer.operation(node.nodo))
        index += 1 

    errores_semantico = executer.executer_errors

    if not errores_semantico:
        for outs in executer.outputs:
            #print(outs)
            outs_list.append(outs)
    else:
        for error in errores_semantico:
            message = (
            f"Error: {error['code']} en la Línea: {error['line']}, Columna: {error['col']}."
        )
    for name, symbol in executer.symboltable.symbol.items():
        print(f"Variable: {name}, Type: {symbol['type']}, Value: {symbol['value']}")
    
    return message,outs_list