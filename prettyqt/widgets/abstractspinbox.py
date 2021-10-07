from __future__ import annotations

from typing import Literal

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


CORRECTION_MODES = bidict(
    to_previous=QtWidgets.QSpinBox.CorrectionMode.CorrectToPreviousValue,
    to_nearest=QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue,
)

CorrectionModeStr = Literal["to_previous", "to_nearest"]

SYMBOLS = bidict(
    up_down=QtWidgets.QSpinBox.ButtonSymbols.UpDownArrows,
    plus_minus=QtWidgets.QSpinBox.ButtonSymbols.PlusMinus,
    none=QtWidgets.QSpinBox.ButtonSymbols.NoButtons,
)

SymbolStr = Literal["up_down", "plus_minus", "none"]

STEP_TYPES = bidict(
    default=QtWidgets.QSpinBox.StepType.DefaultStepType,
    adaptive=QtWidgets.QSpinBox.StepType.AdaptiveDecimalStepType,
)

StepTypeStr = Literal["default", "adaptive"]


QtWidgets.QAbstractSpinBox.__bases__ = (widgets.Widget,)


class AbstractSpinBox(QtWidgets.QAbstractSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLineEdit(widgets.LineEdit())
        self.setGroupSeparatorShown(True)

    def serialize_fields(self):
        return dict(
            button_symbols=self.get_button_symbols(),
            correction_mode=self.get_correction_mode(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.set_correction_mode(state["correction_mode"])
        self.set_button_symbols(state["button_symbols"])

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(self, validator: gui.Validator):
        self.lineEdit().setValidator(validator)

    def get_button_symbols(self) -> SymbolStr:
        """Return button symbol type.

        Returns:
            button symbol type
        """
        return SYMBOLS.inverse[self.buttonSymbols()]

    def set_button_symbols(self, mode: SymbolStr):
        """Set button symbol type.

        Args:
            mode: button symbol type to use

        Raises:
            InvalidParamError: invalid button symbol type
        """
        if mode not in SYMBOLS:
            raise InvalidParamError(mode, SYMBOLS)
        self.setButtonSymbols(SYMBOLS[mode])

    def set_correction_mode(self, mode: CorrectionModeStr):
        """Set correction mode.

        Args:
            mode: correction mode to use

        Raises:
            InvalidParamError: invalid correction mode
        """
        if mode not in CORRECTION_MODES:
            raise InvalidParamError(mode, CORRECTION_MODES)
        self.setCorrectionMode(CORRECTION_MODES[mode])

    def get_correction_mode(self) -> CorrectionModeStr:
        """Return correction mode.

        Returns:
            correction mode
        """
        return CORRECTION_MODES.inverse[self.correctionMode()]

    def set_step_type(self, mode: StepTypeStr):
        """Set step type.

        Args:
            mode: step type to use

        Raises:
            InvalidParamError: invalid step type
        """
        if mode not in STEP_TYPES:
            raise InvalidParamError(mode, STEP_TYPES)
        self.setStepType(STEP_TYPES[mode])

    def get_step_type(self) -> StepTypeStr:
        """Return step type.

        Returns:
            step type
        """
        return STEP_TYPES.inverse[self.stepType()]

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
    app.main_loop()
