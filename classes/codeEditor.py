from PyQt5.QtWidgets import (
    QPlainTextEdit, QWidget,
    QTextEdit, 
    QTextEdit,
)
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtCore import Qt, QRect, QSize, QRegularExpression


# Clase para el resaltado de sintaxis
class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)
        
        # Formato para palabras clave
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)
        
        # Palabras clave
        keywords = ["int", "string", "boolean", "if", "else", "while", "for", "true", "false", "print"]
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







