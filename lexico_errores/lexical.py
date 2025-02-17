import pandas as pd

#POSICION 
#global line, col, stack_col, pila_cadena


def lexical_analysis(archivo):
    global line, col, stack_col, pila_cadena

    line = 1
    col = 0
    stack_col =[]

    # read by default 1st sheet of an excel file
    matrix = pd.read_excel('lexico_errores/matriz.xlsx')
    spaces =  [' ', '\t', '\n']
    pila_comillas = []
    pila_cadena =[]
    alphabet = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "_", "<", ">", "=", "!", "&", "|", "+", "-", "*", "/", "(", ")", "{", "}",
        "[", "]", "\"", ".", " ", "jmp", "tab",";",","
    ]
    
    result = []
    stack_error = []

    with open(archivo, 'r') as file:
        # Crear una lista para almacenar los caracteres
        token = ""
        row = 0     #Estado = 0
        while True:
            # Leer un solo carácter
            char = file.read(1)
            # Si no hay más caracteres, salir del bucle
            if not char:
                #Verifica que haya un token al final del archivo
                #Si no es Entero
                if isinstance(matrix["jmp"][row], int):
                    error = matrix["jmp"][row]
                    #print (error)
                    if (error == 68):
                        error = 1018
                        #print (error)
                    if (error == 66 or error == 67):
                        error = 1019
                        #print (error)
                    if(error>999):
                        col_pos = col - len(token)+1
                        row_pos = line
                        if(pila_comillas):
                            col_pos = pila_cadena[0][1]
                            row_pos = pila_cadena[0][0]
                        if (error == 1019): 
                            col_pos = col +1
                        get_errors(stack_error,error, col_pos,row_pos,"-f")
                        #print(stack_error)
                    
                else:
                    col_pos = col - len(token)
                    row_pos = line
                    if(not pila_comillas and pila_cadena):
                        col_pos = pila_cadena[0][1]-1
                        row_pos = pila_cadena[0][0]
                    result.append([token,matrix["jmp"][row],row_pos,col_pos+1])   
                result.append(["end","end",row_pos,col_pos])
                break
            #procesa el caracter para ser entendido por la matriz
            column = procesar_char(char)


            if column not in alphabet:
                col_pos = col
                row_pos = line
                get_errors(stack_error,1000, col_pos,row_pos,"-c")
                column = " "
                char=""
                  # Romper el bucle si no está permitido
            
            #agrega contenido al token
            if isinstance(matrix[column][row], int):
                if (matrix[column][row]>=1000):
                    if(col < 2):
                        col_pos = stack_col[-1] - len(token)
                        row_pos = line -1
                    else:
                        col_pos = col - len(token)
                        row_pos = line

                    get_errors(stack_error,matrix[column][row], col_pos,row_pos,"-p")
                    row = matrix[column][0]
                    token = ""
                    row = 0
                
                row = matrix[column][row]
                if char == "\"":
                    if not pila_comillas:
                        pila_comillas.append(char)  # Abrir comillas
                        pila_cadena.append([line,col])
                    else:
                        pila_comillas.pop()  # Cerrar comillas
                else:    
                    if char not in spaces:
                        token += char
                    elif  pila_comillas:
                        token += char
                
            else:
                #lo cambian por un almacenamiento en la tabla, asi como tambien la posicion
                if(col < 2):
                    col_pos = stack_col[-1] - len(token)
                    row_pos = line -1
                else:
                    col_pos = col - len(token)
                    row_pos = line
                if(not pila_comillas and pila_cadena):
                    col_pos = pila_cadena[0][1]
                    row_pos = pila_cadena[0][0]
                    pila_cadena.pop()
        
                result.append([token,matrix[column][row],row_pos, col_pos])
                
                token = ""
                row = 0
                if char not in spaces :
                    row = matrix[column][row]
                    if char == "\"":
                        if not pila_comillas:
                            pila_comillas.append(char)  # Abrir comillas
                            pila_cadena.append([line,col])
                        else:
                            pila_comillas.pop()  # Cerrar comillas
                    else:    
                        if char not in spaces:
                            token += char
                        elif  pila_comillas:
                            token += char

                    #No es un entero, por lo tanto es 
                    if  not isinstance(matrix[column][row], int) :
                        #Obtener posicion inicial del token
                        col_pos = col - len(token)
                        result.append([token,matrix[column][row],line,col_pos+1])
                        token = ""
                        row = 0
    return result,stack_error

#Determina la columna del autómata y actualiza posición global.
def procesar_char(char):
    global line, col
    col += 1  # Incrementar columna por carácter leído
    if char.isdigit():
        column = int(char)
    else:
        column = str(char)
        

    if char == "\n":
        column = "jmp"
        stack_col.append(col)

        line += 1
        col = 0  # Reiniciar columna en nueva línea
    elif char == "\t":
        column = "tab"
        col += 3  # 1 tab = 4 espacios
    return column

def get_errors(stack_error,code, col,line,place):
    stack_error.append({"code": code, "line": line, "col": col, "place":place})

if __name__ == '__main__':
    file = 'source_code.txt'
    result = lexical_analysis(file)[0]
    for i in result:
        print(i)

