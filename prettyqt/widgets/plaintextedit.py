# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtWidgets

from prettyqt import gui, widgets, core


QtWidgets.QPlainTextEdit.__bases__ = (widgets.AbstractScrollArea,)


class PlainTextEdit(QtWidgets.QPlainTextEdit):

    value_changed = core.Signal()

    def __init__(self, text="", parent=None, read_only=False):
        super().__init__(text, parent)
        self.textChanged.connect(self.value_changed)
        self.set_read_only(read_only)

    def __getstate__(self):
        return dict(text=self.text(),
                    enabled=self.isEnabled(),
                    read_only=self.isReadOnly(),
                    font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.__init__()
        self.set_text(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])
        self.setReadOnly(state["read_only"])

    def __add__(self, other):
        if isinstance(other, str):
            self.append_text(other)
            return self

    def append_text(self, text: str):
        self.appendPlainText(text)

    def set_text(self, text: str):
        self.setPlainText(text)

    def text(self) -> str:
        return self.toPlainText()

    def set_read_only(self, value: bool = True):
        """set test to read only

        Args:
            value: True, for read-only, otherwise False
        """
        self.setReadOnly(value)

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

    @classmethod
    def get_result_widget(cls, *args, **kwargs):
        widget = cls(*args, **kwargs)
        widget.setReadOnly(True)
        widget.set_font("Consolas")
        return widget

    def set_value(self, value: str):
        self.setPlainText(value)

    def get_value(self):
        return self.text()


if __name__ == "__main__":
    app = widgets.app()
    widget = PlainTextEdit("This is a test")
    widget.show()
    app.exec_()
