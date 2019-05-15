# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, core


class SpinBox(QtWidgets.QSpinBox):

    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())
        self.valueChanged.connect(self.value_changed)
        self.setGroupSeparatorShown(True)

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
        self.setRange(*state["range"])
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


SpinBox.__bases__[0].__bases__ = (widgets.AbstractSpinBox,)


if __name__ == "__main__":
    app = widgets.app()
    widget = SpinBox()
    widget.show()
    app.exec_()
