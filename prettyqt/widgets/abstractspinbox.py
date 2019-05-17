# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets

from prettyqt import widgets, gui

CORRECTION_MODES = bidict(dict(to_previous=QtWidgets.QSpinBox.CorrectToPreviousValue,
                               to_nearest=QtWidgets.QSpinBox.CorrectToNearestValue))

SYMBOLS = bidict(dict(up_down=QtWidgets.QSpinBox.UpDownArrows,
                      plus_minus=QtWidgets.QSpinBox.PlusMinus,
                      none=QtWidgets.QSpinBox.NoButtons))

STEP_TYPES = bidict(dict(default=QtWidgets.QSpinBox.DefaultStepType,
                         adaptive=QtWidgets.QSpinBox.AdaptiveDecimalStepType))


class AbstractSpinBox(QtWidgets.QAbstractSpinBox):

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(self, validator: gui.Validator):
        self.lineEdit().setValidator(validator)

    def get_button_symbols(self) -> str:
        return SYMBOLS.inv[self.buttonSymbols()]

    def set_button_symbols(self, mode: str):
        self.setButtonSymbols(SYMBOLS[mode])

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

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        self.setValue(value)


AbstractSpinBox.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractSpinBox()
    widget.show()
    app.exec_()
