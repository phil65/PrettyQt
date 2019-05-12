# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, gui

CORRECTION_MODES = dict(to_previous=QtWidgets.QSpinBox.CorrectToPreviousValue,
                        to_nearest=QtWidgets.QSpinBox.CorrectToNearestValue)

SYMBOLS = dict(up_down=QtWidgets.QSpinBox.UpDownArrows,
               plus_minus=QtWidgets.QSpinBox.PlusMinus,
               none=QtWidgets.QSpinBox.NoButtons)

STEP_TYPES = dict(default=QtWidgets.QSpinBox.DefaultStepType,
                  adaptive=QtWidgets.QSpinBox.AdaptiveDecimalStepType)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())
        self.setGroupSeparatorShown(True)

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    enabled=self.isEnabled(),
                    step_type=self.get_step_type(),
                    prefix=self.prefix(),
                    suffix=self.suffix(),
                    single_step=self.singleStep())

    def __setstate__(self, state):
        self.__init__()
        self.setRange(*state["range"])
        self.setValue(state["value"])
        self.setEnabled(state["enabled"])
        self.setPrefix(state["prefix"])
        self.setSuffix(state["suffix"])
        self.setSingleStep(state["single_step"])
        self.set_step_type(state["step_type"])

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

    def set_correction_mode(self, mode: str):
        self.setCorrectionMode(CORRECTION_MODES[mode])

    def set_step_type(self, mode: str):
        self.setStepType(STEP_TYPES[mode])

    def get_step_type(self):
        return STEP_TYPES.inv[self.stepType()]

    def set_special_value(self, value: str):
        self.setSpecialValueText(value)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = DoubleSpinBox()
    widget.show()
    app.exec_()
