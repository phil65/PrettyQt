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


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    value_changed = core.Signal(float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.value_changed)
        self.setLineEdit(widgets.LineEdit())
        self.setGroupSeparatorShown(True)

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    enabled=self.isEnabled(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    step_type=self.get_step_type(),
                    prefix=self.prefix(),
                    correction_mode=self.get_correction_mode(),
                    button_symbols=self.get_button_symbols(),
                    decimals=self.decimals(),
                    suffix=self.suffix(),
                    single_step=self.singleStep())

    def __setstate__(self, state):
        self.__init__()
        self.setRange(*state["range"])
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

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(self, validator: gui.Validator):
        self.lineEdit().setValidator(validator)

    def set_button_symbols(self, mode: str):
        self.setButtonSymbols(SYMBOLS[mode])

    def get_button_symbols(self) -> str:
        return SYMBOLS.inv[self.buttonSymbols()]

    def set_correction_mode(self, mode: str):
        self.setCorrectionMode(CORRECTION_MODES[mode])

    def get_correction_mode(self) -> str:
        return CORRECTION_MODES.inv[self.correctionMode()]

    def set_step_type(self, mode: str):
        self.setStepType(STEP_TYPES[mode])

    def get_step_type(self) -> str:
        return STEP_TYPES.inv[self.stepType()]

    def set_special_value(self, value: str):
        self.setSpecialValueText(value)

    def get_value(self) -> float:
        return self.value()

    def set_value(self, value):
        self.setValue(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = DoubleSpinBox()
    widget.show()
    app.exec_()
