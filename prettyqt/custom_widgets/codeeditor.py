from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets


class CodeEditor(widgets.PlainTextEdit):
    def __init__(self, language: str = "python", parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_area_width)
        self.updateRequest.connect(self.update_line_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.set_font("Consolas")
        self.update_line_area_width(0)
        self.highlight_current_line()
        self.set_syntaxhighlighter(language)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        rect = core.Rect(cr.left(), cr.top(), self.line_area_width(), cr.height())
        self.line_area.setGeometry(rect)

    def text(self) -> str:
        return self.toPlainText()

    def line_area_width(self) -> int:
        digits = len(str(self.blockCount()))
        return 3 + self.fontMetrics().boundingRect("9").width() * digits

    def update_line_area_width(self, _):
        self.setViewportMargins(self.line_area_width(), 0, 0, 0)

    def update_line_area(self, rect: QtCore.QRect, dy: int):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_area_width(0)

    def line_area_paintevent(self, event):
        with gui.Painter(self.line_area) as painter:
            painter.fill_rect(event.rect(), "lightgray")

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
                    painter.drawText(
                        0, int(top), width, height, constants.ALIGN_RIGHT, number
                    )
                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1


class LineNumberArea(widgets.Widget):
    def __init__(self, editor: CodeEditor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> core.Size:
        return core.Size(self.editor.line_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_area_paintevent(event)


if __name__ == "__main__":
    app = widgets.app()
    dlg = CodeEditor()
    dlg.show()
    app.main_loop()
