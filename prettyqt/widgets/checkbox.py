# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class CheckBox(QtWidgets.QCheckBox):

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

    def get_value(self):
        return self.isChecked()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = CheckBox("test")
    widget.show()
    app.exec_()
