# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtGui
from prettyqt import widgets, gui


class PlainTextEdit(QtWidgets.QPlainTextEdit):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_font(self,
                 font_name: str,
                 font_size: int = -1,
                 weight: int = -1,
                 italic: bool = False):
        font = QtGui.QFont(font_name, font_size, weight, italic)
        self.setFont(font)

    def append(self, text: str):
        self.appendPlainText(text)

    def set_text(self, text: str):
        self.setPlainText(text)

    def text(self) -> str:
        return self.toPlainText()

    def set_read_only(self, value: bool):
        """set test to read only

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

    def scroll_to_end(self):
        """scroll to the end of the text
        """
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = widgets.TextEdit.ExtraSelection()
            line_color = gui.Color("yellow").lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = PlainTextEdit("This is a test")
    widget.show()
    app.exec_()
