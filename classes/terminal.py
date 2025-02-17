import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit
)
from PyQt5.QtCore import pyqtSlot


class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def clear_terminal(self):
        """Limpia el contenido de la terminal."""
        self.output_area.clear()

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta para mostrar la ruta actual
        self.path_label = QLabel()
        self.update_path()

        # Campo de entrada para comandos
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Escribe un comando y presiona Enter")
        self.command_input.returnPressed.connect(self.execute_command)

        # Área de texto para mostrar la salida
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)

        # Agregar widgets al layout
        layout.addWidget(self.path_label)
        layout.addWidget(self.command_input)
        layout.addWidget(self.output_area)
        self.setLayout(layout)

    def update_path(self):
        """Actualiza la etiqueta con la ruta actual."""
        current_path = os.getcwd()
        self.path_label.setText(f"Ruta actual: {current_path}")

    @pyqtSlot()
    def execute_command(self):
        """Ejecuta el comando ingresado y muestra el resultado."""
        command = self.command_input.text().strip()
        if command:
            try:
                # Ejecutar el comando y capturar la salida
                output = os.popen(command).read()
                self.output_area.appendPlainText(f"$ {command}")
                self.output_area.appendPlainText(output)
            except Exception as e:
                self.output_area.appendPlainText(f"Error al ejecutar el comando: {e}")
            finally:
                self.command_input.clear()

    def set_initial_path(self, path):
        """Permite configurar una ruta inicial."""
        try:
            os.chdir(path)
            self.update_path()
        except Exception as e:
            self.output_area.appendPlainText(f"Error al cambiar de directorio: {e}")

    def append_message(self, message):
        """Añade un mensaje a la terminal."""
        self.output_area.appendPlainText(message)
