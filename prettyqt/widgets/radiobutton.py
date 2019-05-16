# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets
from prettyqt import core, widgets


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def __bool__(self):
        return self.isChecked()

    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value: bool):
        self.setChecked(value)


RadioButton.__bases__[0].__bases__ = (widgets.AbstractButton,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
