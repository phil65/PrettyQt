# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets
from prettyqt import core


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def __repr__(self):
        return f"RadioButton: {self.__getstate__()}"

    def __getstate__(self):
        return dict(checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    text=self.text(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__init__()
        self.setChecked(state["checked"])
        self.setText(state["text"])
        self.setEnabled(state["enabled"])
        self.setCheckable(state["checkable"])

    def __bool__(self):
        return self.isChecked()

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def get_value(self):
        return self.isChecked()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = RadioButton("This is a test")
    widget.set_icon("mdi.timer")
    widget.show()
    app.exec_()
