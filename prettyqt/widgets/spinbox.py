# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets

from prettyqt import widgets, gui, core

CORRECTION_MODES = bidict(dict(to_previous=QtWidgets.QSpinBox.CorrectToPreviousValue,
                               to_nearest=QtWidgets.QSpinBox.CorrectToNearestValue))

SYMBOLS = bidict(dict(up_down=QtWidgets.QSpinBox.UpDownArrows,
                      plus_minus=QtWidgets.QSpinBox.PlusMinus,
                      none=QtWidgets.QSpinBox.NoButtons))

STEP_TYPES = bidict(dict(default=QtWidgets.QSpinBox.DefaultStepType,
                         adaptive=QtWidgets.QSpinBox.AdaptiveDecimalStepType))


class SpinBox(QtWidgets.QSpinBox):

    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())
        self.valueChanged.connect(self.value_changed)
        self.setGroupSeparatorShown(True)

    def __repr__(self):
        return f"SpinBox: {self.__getstate__()}"

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
        self.setEnabled(state["enabled"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])
        self.setSingleStep(state["single_step"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.set_button_symbols(state["button_symbols"])
        self.set_correction_mode(state["correction_mode"])
        self.setDisplayIntegerBase(state["int_base"])
        self.set_step_type(state["step_type"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(self, validator: gui.Validator):
        self.lineEdit().setValidator(validator)

    def get_button_symbols(self):
        return SYMBOLS.inv[self.buttonSymbols()]

    def set_button_symbols(self, mode: str):
        self.setButtonSymbols(SYMBOLS[mode])

    def set_correction_mode(self, mode: str):
        self.setCorrectionMode(CORRECTION_MODES[mode])

    def get_correction_mode(self):
        return CORRECTION_MODES.inv[self.correctionMode()]

    def set_step_type(self, mode: str):
        self.setStepType(STEP_TYPES[mode])

    def get_step_type(self):
        return STEP_TYPES.inv[self.stepType()]

    def set_special_value(self, value: str):
        self.setSpecialValueText(value)

    def get_value(self):
        return self.value()

    def set_value(self, value):
        self.setValue(value)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = SpinBox()
    widget.show()
    app.exec_()
