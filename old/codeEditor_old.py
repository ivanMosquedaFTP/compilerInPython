import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QTextEdit, QAction,
    QApplication,
    QFileDialog,
    QMainWindow,
    QTextEdit,
    QMenuBar
)
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QSyntaxHighlighter, QTextCharFormat, QFont, QPalette
from PyQt5.QtCore import Qt, QRect, QSize, QRegularExpression

import toolBar

from a_lex import analyze  # Asegúrarse de que `a_lex` contiene la función `analyze`

# Clase para el resaltado de sintaxis
class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)
        
        # Formato para palabras clave
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)
        
        # Palabras clave
        keywords = ["int", "string", "boolean", "if", "else", "while", "for", "true", "false"]
        self.highlighting_rules = [(QRegularExpression(r"\b" + keyword + r"\b"), keyword_format) for keyword in keywords]
        
        # Formato para literales de cadena
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("darkGreen"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        
        # Formato para literales de números
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("darkMagenta"))
        self.highlighting_rules.append((QRegularExpression(r"\b\d+\b"), number_format))
        
    def highlightBlock(self, text):
        # Aplicar cada regla de resaltado
        for pattern, fmt in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iter = expression.globalMatch(text)
            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class CodeEditor(QPlainTextEdit):
    def __init__(self, symbol_table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_number_area = LineNumberArea(self)
        self.symbol_table = symbol_table
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

        # Aplicar resaltado de sintaxis
        self.highlighter = SyntaxHighlighter(self.document())

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * (digits + 1)
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.line_number_area.width(), int(self.fontMetrics().height()), Qt.AlignRight, str(number))

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class SymbolTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Tabla de Símbolos")
        layout.addWidget(label)

        # Crear la tabla con las columnas requeridas
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Tipo", "Valor", "Línea", "Columna"])
        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_symbols(self, tokens):
        self.table.setRowCount(0)  # Borrar datos anteriores

        # Variables para almacenar el estado actual
        current_type = None
        current_identifier = None
        current_value = "NULL"  # Valor predeterminado
        expecting_value = False  # Indica si estamos esperando un valor después de '='
        found_name = False  # Indica si ya hemos encontrado el nombre de la variable

        # Recorrer los tokens para identificar declaraciones de variables
        for token in tokens:
            token_value, token_type, line, column = token

            if token_type in ["INT", "STRING", "BOOLEAN"]:
                current_type = token_value  # Captura el tipo de dato

            elif token_type == "IDENTIFIER" and current_type and not found_name:
                # Captura el identificador después de declarar el tipo como nombre de la variable
                current_identifier = token_value
                found_name = True  # Marcar que hemos encontrado el nombre de la variable

            elif token_type == "ASSIGN" and current_identifier:
                # Indica que el siguiente token debe ser el valor asignado
                expecting_value = True

            elif expecting_value:
                # Si estamos esperando un valor, verificar si es compatible con el tipo
                if current_type == "int" and token_type == "INT_LITERAL":
                    current_value = token_value
                #elif current_type == "float" and token_type == "FLOAT_LITERAL":
                #    current_value = token_value
                elif current_type == "boolean" and token_value in ["true", "false"]:
                    current_value = token_value
                elif current_type == "string" and token_type == "STRING_LITERAL":
                    current_value = token_value.strip('"')
                else:
                    # Si el valor no es compatible, lo dejamos como "NULL"
                    current_value = "NULL"
                expecting_value = False

            elif token_type == "SEMICOLON" and found_name:
                # Solo ahora agregamos a la tabla de símbolos si todo es correcto
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(current_identifier))
                self.table.setItem(row_position, 1, QTableWidgetItem(current_type))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(current_value)))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(line)))
                self.table.setItem(row_position, 4, QTableWidgetItem(str(column)))

                # Restablece los valores después de agregar la variable
                current_identifier = None
                current_type = None
                current_value = "NULL"
                expecting_value = False
                found_name = False  # Listo para la próxima declaración

        # Actualización forzada de la tabla de símbolos
        self.table.viewport().update()



class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.symbol_table = SymbolTable()
        self.editor = CodeEditor(self.symbol_table)
        self.tool_bar = toolBar(self.editor)

        # Crear botón de "Compilar"
        
        compile_button = QPushButton("Compilar", self)
        compile_button.clicked.connect(self.compile_code)

        """
        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFixedHeight(150)  # Ajusta la altura de la terminal
        
        # Configurar el color de fondo y del texto
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0))  # Fondo negro
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # Texto blanco
        self.terminal_output.setPalette(palette)
        """
        #Terminal
        

        # Layout para dividir el editor de código y la tabla de símbolos
        layout = QVBoxLayout()
        editor_layout = QHBoxLayout()
        editor_layout.addWidget(self.tool_bar)
        editor_layout.addWidget(self.editor)
        editor_layout.addWidget(self.symbol_table)

        layout.addWidget(compile_button)  # Añadir el botón al layout principal
        layout.addLayout(editor_layout)   # Añadir el layout del editor y tabla al layout principal
        

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("IDE C+|- ")
        self.setGeometry(100, 100, 1150, 600)

    def compile_code(self):
        # Obtener el contenido del editor
        src = self.editor.toPlainText()
        
        # Guardar el contenido en un archivo .txt
        try:
            with open("output_code.txt", "w", encoding="utf-8") as file:
                file.write(src)
            print("El código se ha guardado exitosamente en output_code.txt")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

        tokens = analyze(src)
        self.symbol_table.update_symbols(tokens)


def main():
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())

