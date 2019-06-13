# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, gui
from prettyqt.utils import bidict


CORRECTION_MODES = bidict(to_previous=QtWidgets.QSpinBox.CorrectToPreviousValue,
                          to_nearest=QtWidgets.QSpinBox.CorrectToNearestValue)

SYMBOLS = bidict(up_down=QtWidgets.QSpinBox.UpDownArrows,
                 plus_minus=QtWidgets.QSpinBox.PlusMinus,
                 none=QtWidgets.QSpinBox.NoButtons)

STEP_TYPES = bidict(default=QtWidgets.QSpinBox.DefaultStepType,
                    adaptive=QtWidgets.QSpinBox.AdaptiveDecimalStepType)


QtWidgets.QAbstractSpinBox.__bases__ = (widgets.Widget,)


class AbstractSpinBox(QtWidgets.QAbstractSpinBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())
        self.setGroupSeparatorShown(True)

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(self, validator: gui.Validator):
        self.lineEdit().setValidator(validator)

    def get_button_symbols(self) -> str:
        """returns button symbol type

        possible values are "none", "up_down", "plus_minus"

        Returns:
            button symbol type
        """
        return SYMBOLS.inv[self.buttonSymbols()]

    def set_button_symbols(self, mode: str):
        """sets button symbol type

        possible values are "none", "up_down", "plus_minus"

        Args:
            mode: button symbol type to use

        Raises:
            ValueError: invalid button symbol type
        """
        if mode not in SYMBOLS:
            raise ValueError("Invalid button symbol type.")
        self.setButtonSymbols(SYMBOLS[mode])

    def set_correction_mode(self, mode: str):
        """sets correction mode

        possible values are "to_previous", "to_nearest"

        Args:
            mode: correction mode to use

        Raises:
            ValueError: invalid correction mode
        """
        if mode not in CORRECTION_MODES:
            raise ValueError("Invalid correction mode.")
        self.setCorrectionMode(CORRECTION_MODES[mode])

    def get_correction_mode(self) -> str:
        """returns correction mode

        possible values are "to_previous", "to_nearest"

        Returns:
            correction mode
        """
        return CORRECTION_MODES.inv[self.correctionMode()]

    def set_step_type(self, mode: str):
        """sets step type

        possible values are "default", "adaptive"

        Args:
            mode: step type to use

        Raises:
            ValueError: invalid step type
        """
        if mode not in STEP_TYPES:
            raise ValueError("Invalid step type.")
        self.setStepType(STEP_TYPES[mode])

    def get_step_type(self) -> str:
        """returns step type

        possible values are "default", "adaptive"

        Returns:
            step type
        """
        return STEP_TYPES.inv[self.stepType()]

    def set_special_value(self, value: str):
        self.setSpecialValueText(value)

    def get_value(self) -> int:
        return self.value()

    def set_value(self, value: int):
        self.setValue(value)


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractSpinBox()
    widget.show()
    app.exec_()
