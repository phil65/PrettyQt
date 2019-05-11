# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core, gui, syntaxhighlighters, widgets


class LineNumberArea(widgets.Widget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return core.Size(self.editor.line_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_area_paintevent(event)


class CodeEditor(widgets.PlainTextEdit):

    lexers = {"python": syntaxhighlighters.PythonHighlighter,
              "yaml": syntaxhighlighters.JsonHighlighter,
              "json": syntaxhighlighters.YamlHighlighter}
    supported_langs = lexers.keys()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_area_width)
        self.updateRequest.connect(self.update_line_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.set_font("Consolas")

        self.update_line_area_width(0)
        self.highlight_current_line()
        self.highlighter = self.lexers["python"](self.document())

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        rect = core.Rect(cr.left(), cr.top(), self.line_area_width(), cr.height())
        self.line_area.setGeometry(rect)

    def text(self) -> str:
        return self.toPlainText()

    def line_area_width(self) -> int:
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width("9") * digits
        return space

    def update_line_area_width(self, _):
        self.setViewportMargins(self.line_area_width(), 0, 0, 0)

    def update_line_area(self, rect, dy):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_area_width(0)

    def line_area_paintevent(self, event):
        painter = gui.Painter(self.line_area)
        painter.fillRect(event.rect(), gui.Color("lightgray"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        width = self.line_area.width()
        height = self.fontMetrics().height()
        painter.set_color("black")
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                painter.drawText(0, top, width, height, QtCore.Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def set_syntax(self, language: str):
        lexer = self.lexers[language]
        self.highlighter = lexer(self.document())


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    dlg = CodeEditor()
    dlg.show()
    app.exec_()
