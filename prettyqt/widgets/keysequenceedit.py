# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtGui, QtWidgets

from prettyqt import core, gui, widgets


QtWidgets.QKeySequenceEdit.__bases__ = (widgets.Widget,)


class KeySequenceEdit(QtWidgets.QKeySequenceEdit):

    value_changed = core.Signal(QtGui.QKeySequence)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keySequenceChanged.connect(self.value_changed)

    def __repr__(self):
        return f"KeySequenceEdit({self.get_value()})"

    def set_value(self, value: str):
        seq = gui.KeySequence.fromString(value)
        self.setKeySequence(seq)

    def get_value(self) -> str:
        return self.keySequence().toString()

    def is_valid(self) -> bool:
        return True


if __name__ == "__main__":
    app = widgets.app()
    widget = KeySequenceEdit()
    widget.show()
    app.exec_()
