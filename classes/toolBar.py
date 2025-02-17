from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QFileDialog,
    QMenuBar,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout
)
from PyQt5.QtWidgets import QLabel, QDialog, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt 
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont

class ToolBar(QMainWindow):
    def __init__(self, editor, parent=None):
        super().__init__()

        self.setWindowTitle("Text Editor with Toolbar")

        # Editor de texto como widget central
        self.editor = editor
        self.setCentralWidget(self.editor)

        # Variables para almacenar tokens y errores
        self.tokens = []
        self.errors = []
        self.errors = []  # Lista para almacenar la pila de errores

        # Crear barra de menús
        self.create_menus()

    def create_menus(self):
        # Crear barra de menú
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menú File
        file_menu = menu_bar.addMenu("&File")

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        

        file_menu.addSeparator()


        # Menú Window
        win_menu = menu_bar.addMenu("&Window")

        show_token_table_action = QAction("Show Token Table", self)
        show_token_table_action.triggered.connect(self.show_token_table)
        win_menu.addAction(show_token_table_action)
        
         # Acción para mostrar la pila de errores
        show_error_stack_action = QAction("Show Error Stack", self)
        show_error_stack_action.triggered.connect(self.show_error_stack)
        win_menu.addAction(show_error_stack_action)


        # Menú Help
        help_menu = menu_bar.addMenu("&Help")
        # Acción para mostrar los integrantes del grupo
        group_members_action = QAction("Equipo", self)
        group_members_action.triggered.connect(self.show_group_members)
        help_menu.addAction(group_members_action)

        lex_analysis_action = QAction("Analizador Lexico", self)
        lex_analysis_action.triggered.connect(self.open_lexical_analysis_pdf)
        help_menu.addAction(lex_analysis_action)

        sint_analysis_action = QAction("Analizador Sintactico", self)
        sint_analysis_action.triggered.connect(self.open_sint_analysis_pdf)
        help_menu.addAction(sint_analysis_action)

        sem_analysis_action = QAction("Analizador Semantico", self)
        sem_analysis_action.triggered.connect(self.open_sem_analysis_pdf)
        help_menu.addAction(sem_analysis_action)

    def open_file(self):
        # Abrir cuadro de diálogo para seleccionar archivo
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.editor.setPlainText(content)  # Método correcto para QPlainTextEdit o QTextEdit
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")

    def save_file(self):
        # Abrir cuadro de diálogo para guardar archivo
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.editor.toPlainText()
                    file.write(content)
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")

    def run_code(self):
        content = self.editor.toPlainText()
        try:
            with open("source_code.txt", "w", encoding="utf-8") as file:
                file.write(content)
            from lexico_errores.my_lex import lex_analyze
            result = lex_analyze("source_code.txt")
            self.tokens = result[0]
            self.errors = result[1]
        except Exception as e:
            print(f"Error en el análisis: {e}")

    def show_token_table(self):
            dialog = QDialog(self)
            dialog.setWindowTitle("Token Table")
            layout = QVBoxLayout()
            table = QTableWidget(len(self.tokens), 4)
            table.setHorizontalHeaderLabels(["Token", "Type", "Line", "Column"])
            
            for i, token in enumerate(self.tokens):
                if isinstance(token, list):  # Caso en el que los tokens sean listas
                    table.setItem(i, 0, QTableWidgetItem(str(token[0])))  # Token
                    table.setItem(i, 1, QTableWidgetItem(str(token[1])))  # Type
                    table.setItem(i, 2, QTableWidgetItem(str(token[2])))  # Line
                    table.setItem(i, 3, QTableWidgetItem(str(token[3])))  # Column
                elif isinstance(token, dict):  # Caso en el que los tokens sean diccionarios
                    table.setItem(i, 0, QTableWidgetItem(token.get('token', '')))
                    table.setItem(i, 1, QTableWidgetItem(token.get('type', '')))
                    table.setItem(i, 2, QTableWidgetItem(str(token.get('line', ''))))
                    table.setItem(i, 3, QTableWidgetItem(str(token.get('column', ''))))
            
            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.resize(600, 400)
            dialog.exec_()
     
     
     
    def add_errors(self, new_errors):
        """Agrega nuevos errores a la pila."""
        self.errors.extend(new_errors)

    def show_error_stack(self):
        """Muestra la pila de errores en un cuadro de diálogo."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Error Stack")
        layout = QVBoxLayout()

        # Crear tabla de errores
        table = QTableWidget(len(self.errors), 5)
        print("Errores actuales:", self.errors)
        table.setHorizontalHeaderLabels(["ID", "Line", "Column", "Message", "Place"])

        for i, error in enumerate(self.errors):
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))  # ID
            table.setItem(i, 1, QTableWidgetItem(str(error.get("line", ""))))  # Line
            table.setItem(i, 2, QTableWidgetItem(str(error.get("column", ""))))  # Column
            table.setItem(i, 3, QTableWidgetItem(error.get("message", "")))  # Message
            table.setItem(i, 4, QTableWidgetItem(error.get("place", "")))  # Place

        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()
        
    def clear_errors(self):
        """Limpia la pila de errores."""
        self.errors = []

    
    def update_data(self, tokens):
        self.tokens = tokens


    #######################################################################################################
    #                                   FUNCIONES PARA ABRIR PDFs
    ######################################################################################################3

    def open_lexical_analysis_pdf(self):
    # Ruta al archivo PDF
        pdf_path = "resources/analisis_lexico.pdf"  # Cambia esta ruta a la ubicación de tu PDF

    # Abrir el archivo PDF usando la aplicación predeterminada
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))

    def open_sint_analysis_pdf(self):
    # Ruta al archivo PDF
        pdf_path = "resources/analisis_sintactico.pdf"  # Cambia esta ruta a la ubicación de tu PDF

    # Abrir el archivo PDF usando la aplicación predeterminada
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
    
    def open_sem_analysis_pdf(self):
    # Ruta al archivo PDF
        pdf_path = "resources/analisis_semantico.pdf"  # Cambia esta ruta a la ubicación de tu PDF

    # Abrir el archivo PDF usando la aplicación predeterminada
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))

    ####################################################################################################
    #                                   FUNCIONES PARA MOSTRAR LOS MIEMBROS DEL EQUIPO
    ####################################################################################################



    def show_group_members(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Group Members")
        layout = QGridLayout()  # Usamos QGridLayout para organizar en cuadrícula

    # Datos de los integrantes (reemplaza las rutas con las correspondientes)
        members = [
            {"name": "Erick Eduardo Acevedo Colunga", "image": "resources/erick.png"},
            {"name": "Adrian Plascencia Fonseca", "image": "resources/adrian.png"},
            {"name": "Cristian Quintana Villicaña", "image": "resources/cris.png"},
            {"name": "Rubén Eliezer Rivera López", "image": "resources/ruben.png"}
        ]

    # Establecer tamaño máximo de las imágenes
        max_width = 500  # Ancho máximo de la imagen
        max_height = 500  # Alto máximo de la imagen

    # Crear fuente personalizada para los nombres
        font = QFont("Arial", 12, QFont.Bold)  # Cambia el nombre de la fuente, tamaño y estilo

    # Agregar las imágenes y los nombres a la cuadrícula
        row, col = 0, 0  # Contadores para fila y columna en la cuadrícula

        for member in members:
        # Crear el nombre con formato
            name_label = QLabel(member["name"], dialog)
            name_label.setFont(font)  # Establecer la fuente al texto

        # Establecer color del texto usando HTML (por ejemplo, rojo)
            name_label.setStyleSheet("color: #333333;")  # Cambiar el color del texto (puedes elegir el color que prefieras)

        # Cargar y redimensionar la imagen
            pixmap = QPixmap(member["image"])
            pixmap = pixmap.scaled(max_width, max_height, aspectRatioMode=True)  # Redimensiona manteniendo la relación de aspecto

        # Crear el QLabel para la imagen
            image_label = QLabel(dialog)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)  # Alineación centrada
            image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Hacer el QLabel redimensionable

        # Agregar la imagen y el nombre a la cuadrícula en la misma fila
            layout.addWidget(image_label, row, col)
            layout.addWidget(name_label, row + 1, col)  # Colocar el nombre debajo de la imagen

        # Incrementar los contadores para la siguiente celda de la cuadrícula
            col += 1
            if col == 4:  # Después de 4 columnas, vamos a la siguiente fila
                col = 0
                row += 2  # Dejar espacio entre la imagen y el nombre

    # Establecer el layout para el diálogo
        dialog.setLayout(layout)
        dialog.resize(500, 600)  # Ajusta el tamaño del diálogo según sea necesario
        dialog.exec_()