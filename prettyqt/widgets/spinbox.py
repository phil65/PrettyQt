# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import core, widgets

QtWidgets.QSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class SpinBox(QtWidgets.QSpinBox):

    value_changed = core.Signal(int)

    def __init__(self, parent=None, min_value=None, max_value=None, default_value=None):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    enabled=self.isEnabled(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    prefix=self.prefix(),
                    suffix=self.suffix(),
                    int_base=self.displayIntegerBase(),
                    step_type=self.get_step_type(),
                    button_symbols=self.get_button_symbols(),
                    correction_mode=self.get_correction_mode(),
                    single_step=self.singleStep())

    def __setstate__(self, state):
        self.__init__()
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setSingleStep(state["single_step"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.set_button_symbols(state["button_symbols"])
        self.set_correction_mode(state["correction_mode"])
        self.setDisplayIntegerBase(state["int_base"])
        self.set_step_type(state["step_type"])

    def set_range(self, start, end):
        if start is None:
            start = -2147483647
        if end is None:
            end = 2147483647
        self.setRange(start, end)

    def set_step_size(self, step_size):
        self.setSingleStep(step_size)


if __name__ == "__main__":
    app = widgets.app()
    widget = SpinBox()
    widget.show()
    app.exec_()
