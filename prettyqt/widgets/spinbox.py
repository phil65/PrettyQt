# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class SpinBox(QtWidgets.QSpinBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())

    def __repr__(self):
        return f"SpinBox: {self.__getstate__()}"

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    enabled=self.isEnabled(),
                    single_step=self.singleStep())

    def __setstate__(self, state):
        super().__init__()
        self.setRange(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state["enabled"])
        self.setSingleStep(state["single_step"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def is_valid(self):
        return self.hasAcceptableInput()

    def set_validator(self, validator):
        self.lineEdit().setValidator(validator)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = SpinBox()
    print(widget)
    widget.show()
    app.exec_()
