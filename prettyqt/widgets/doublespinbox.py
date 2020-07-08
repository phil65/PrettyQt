# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtWidgets

from prettyqt import core, widgets


QtWidgets.QDoubleSpinBox.__bases__ = (widgets.AbstractSpinBox,)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    value_changed = core.Signal(float)

    def __init__(self, parent=None, min_value=None, max_value=None, default_value=None):
        super().__init__(parent)
        self.valueChanged.connect(self.value_changed)
        self.set_range(min_value, max_value)
        if default_value is not None:
            self.set_value(default_value)

    def __getstate__(self):
        return dict(
            range=(self.minimum(), self.maximum()),
            value=super().value(),
            enabled=self.isEnabled(),
            tooltip=self.toolTip(),
            statustip=self.statusTip(),
            step_type=self.get_step_type(),
            prefix=self.prefix(),
            correction_mode=self.get_correction_mode(),
            button_symbols=self.get_button_symbols(),
            decimals=self.decimals(),
            suffix=self.suffix(),
            single_step=self.singleStep(),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_range(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state.get("enabled", True))
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.setDecimals(state["decimals"])
        self.setSingleStep(state["single_step"])
        self.set_step_type(state["step_type"])
        self.set_correction_mode(state["correction_mode"])
        self.set_button_symbols(state["button_symbols"])

    def set_range(self, start, end):
        if start is None:
            start = -float("inf")
        if end is None:
            end = float("inf")
        self.setRange(start, end)


if __name__ == "__main__":
    app = widgets.app()
    widget = DoubleSpinBox()
    widget.show()
    app.exec_()
