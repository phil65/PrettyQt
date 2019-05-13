# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets
from prettyqt import core, gui


class RadioButton(QtWidgets.QRadioButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def __repr__(self):
        return f"RadioButton: {self.__getstate__()}"

    def __getstate__(self):
        return dict(object_name=self.objectName(),
                    checkable=self.isCheckable(),
                    icon=gui.Icon(self.icon()),
                    checked=self.isChecked(),
                    text=self.text(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__init__()
        self.setObjectName(state["object_name"])
        self.set_icon(state["icon"])
        self.setChecked(state["checked"])
        self.setText(state["text"])
        self.setEnabled(state["enabled"])
        self.setCheckable(state["checkable"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])

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
