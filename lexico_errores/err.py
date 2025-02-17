def process_errors(errores):
    result = []
    #lista de errores 
    errors = [
        {"code": 1000, "message": "Caracter no identificado"},
        {"code": 1001, "message": "Los identificadores deben llevar al menos una letra"},
        {"code": 1002, "message": "Los identificadores no pueden empezar con número"},
        {"code": 1003, "message": "Al < solo le puedes concatenar un ="},
        {"code": 1004, "message": "Al <= no le puedes concatenar [<,>,=,!]"},
        {"code": 1005, "message": "Al > solo le puedes concatenar un ="},
        {"code": 1006, "message": "Al >= no le puedes concatenar [<,>,=,!]"},
        {"code": 1007, "message": "Al = solo le puedes concatenar un ="},
        {"code": 1008, "message": "Al == no le puedes concatenar [<,>,=,!]"},
        {"code": 1009, "message": "Al ! solo le puedes concatenar un ="},
        {"code": 1010, "message": "Al != no le puedes concatenar [<,>,=,!]"},
        {"code": 1011, "message": "El & solo puede ir como &&"},
        {"code": 1012, "message": "El && no puede llevar más & concatenados"},
        {"code": 1013, "message": "El | solo puede ir como ||"},
        {"code": 1014, "message": "El || no puede llevar más | concatenados"},
        {"code": 1015, "message": "El ++ no puede llevar + concatenado"},
        {"code": 1016, "message": "El -- no puede llevar - concatenado"},
        {"code": 1017, "message": "El lenguaje solo soporta enteros, favor de solo concatenar números del 0-9"},
        {"code": 1018, "message": "El programa no debe acabar con una cadena abierta"},
        {"code": 1019, "message": "El programa no debe acabar con un comentario abierto"},
    ]
    result = [
        {
            "code": error["code"],
            "line": error["line"],
            "col": error["col"],
            "message": next((e["message"] for e in errors if e["code"] == error["code"]), "Error desconocido"),
            "place":error["place"]
        }
        for error in errores
    ]
    return result



def extract_error_lines(file_path, errores_descriptivos):
    """
    Extrae las líneas específicas del archivo en función de los errores encontrados
    y asocia el mensaje correspondiente al código del error.

    :param file_path: Ruta al archivo de texto.
    :param errores_descriptivos: Lista de diccionarios con los errores (cada uno contiene 'line' y 'col').
    :return: Lista de errores con detalles (línea, columna, contenido, mensaje).
    """
    error_details = []
    with open(file_path, 'r') as file:
        # Leer todas las líneas del archivo
        lines = file.readlines()

        for error in errores_descriptivos:
            line_number = error.get("line")
            col_number = error.get("col")
            message = error.get("message")
            # Validar que la línea existe en el archivo
            if 0 < line_number <= len(lines):
                error_details.append({
                    "line": line_number,
                    "column": col_number,
                    "message": message
                })
    
    return error_details    
 

