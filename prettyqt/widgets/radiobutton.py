# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QRadioButton.__bases__ = (widgets.AbstractButton,)


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def __bool__(self):
        return self.isChecked()

    @property
    def is_on(self) -> bool:
        return self.isChecked()

    @is_on.setter
    def is_on(self, state: bool):
        self.setChecked(state)

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
