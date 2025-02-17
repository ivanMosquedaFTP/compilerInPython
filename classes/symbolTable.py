from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel


class SymbolTable(QWidget):
    def __init__(self):
        super().__init__()
        self.symbols = {}  # Diccionario para almacenar símbolos
        self.initUI()
        self.errors = []   # Lista de errores
      

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Tabla de Símbolos")
        layout.addWidget(label)

        # Crear la tabla con las columnas requeridas
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Tipo", "Valor", "Línea", "Columna"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def clear_table(self):
        """Limpia la tabla de símbolos."""
        self.table.setRowCount(0)  # Limpiar la tabla visual
        self.symbols.clear() 

    def update_symbols(self, tokens):
        self.table.setRowCount(0)  # Borrar datos anteriores

        self.errors = [] # reiniciar errores

        # Diccionario para rastrear variables declaradas
        declared_symbols = {}

        

        current_type = None
        current_identifier = None
        current_value = None

        for token in tokens:
            if len(token) != 4:
                #print(f"Token inválido: {token}")
                self.errors.append(f"Token inválido: {token}")
                continue

            token_value, token_type, line, column = token

            # Capturar tipo de dato
            if token_type in ["int", "string", "boolean"]:
                current_type = token_value

            # Capturar identificador (nombre de variable)
            elif token_type == "id":
                if current_type:  # Nueva declaración
                    if token_value in declared_symbols:
                        # Error: Variable ya declarada
                        self.errors.append(f"Error: La variable '{token_value}' ya fue declarada. Línea: {line}")
                        current_identifier = None
                        current_type = None  # Resetear el tipo
                    else:
                        current_identifier = token_value
                elif token_value in declared_symbols:  # Asignación a variable existente
                    current_identifier = token_value
                else:
                    # Error: Variable no declarada
                    self.errors.append(f"Error: La variable '{token_value}' no ha sido declarada antes de usarse. Línea: {line}")
                    current_identifier = None

            # Detectar asignación
            elif token_type == "asign" and current_identifier:
                continue  # Esperar el valor asignado

            # Capturar valor asignado
            elif current_identifier and token_type in ["number", "chain", "true", "false"]:
                current_value = token_value

            # Finalizar declaración o asignación al encontrar un punto y coma
            elif token_type == "semicolon" and current_identifier:
                if current_identifier in declared_symbols:
                    # Actualizar valor de una variable existente
                    declared_symbols[current_identifier]["value"] = current_value
                    declared_symbols[current_identifier]["line"] = line
                    declared_symbols[current_identifier]["column"] = column
                    #self.errors.append(f"Error: La variable '{token_value}' ya ha sido declarada. Línea: {line}")
                    print(declared_symbols)
                else:
                    # Agregar una nueva variable declarada
                    declared_symbols[current_identifier] = {
                        "type": current_type,
                        "value": current_value,
                        "line": line,
                        "column": column
                    }

                # Actualizar la tabla visual
                self.update_table(declared_symbols)

                # Resetear valores temporales
                current_type = None
                current_identifier = None
                current_value = None

        # Actualización final de la tabla visual
        self.update_table(declared_symbols)

    def get_errors(self):
        if not self.errors:
            print("No hay errores")
            return []
        print(self.errors)
        return self.errors

    def update_table(self, declared_symbols):
        """Actualiza la tabla visual con el contenido del diccionario de símbolos."""
        self.table.setRowCount(0)  # Limpiar la tabla
        for identifier, details in declared_symbols.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(identifier))
            self.table.setItem(row_position, 1, QTableWidgetItem(details["type"] or "N/A"))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(details["value"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(details["line"])))
            self.table.setItem(row_position, 4, QTableWidgetItem(str(details["column"])))
