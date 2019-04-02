# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class TextEdit(QtWidgets.QTextEdit):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_font(self, font):
        self.setFont(font)

    def append(self, text):
        self.appendPlainText(text)

    def set_text(self, text):
        self.setPlainText(text)

    def text(self):
        return self.toPlainText()

    def set_read_only(self, value):
        self.setReadOnly(value)

    def scroll_to_end(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = TextEdit("This is a test")
    widget.show()
    app.exec_()
