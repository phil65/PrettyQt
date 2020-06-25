# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import contextlib

from qtpy import QtWidgets

from prettyqt import gui, core, widgets


QtWidgets.QTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class TextEdit(QtWidgets.QTextEdit):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.on_value_change)

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.__init__()
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    def on_value_change(self):
        self.value_changed.emit(self.text())

    @contextlib.contextmanager
    def create_cursor(self):
        cursor = gui.TextCursor(self.document())
        yield cursor
        self.setTextCursor(cursor)

    def set_text(self, text: str):
        self.setPlainText(text)

    def append_text(self, text: str):
        self.append(text)

    def text(self) -> str:
        return self.toPlainText()

    def select_text(self, start: int, end: int):
        with self.create_cursor() as c:
            c.select_text(start, end)

    def set_read_only(self, value: bool = True):
        self.setReadOnly(value)

    def set_text_color(self, color):
        if isinstance(color, str):
            color = gui.Color(color)
        self.setTextColor(color)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = TextEdit("This is a test")
    widget.show()
    app.exec_()
