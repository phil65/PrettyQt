from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


CorrectionModeStr = Literal["to_previous", "to_nearest"]

CORRECTION_MODES: bidict[CorrectionModeStr, QtWidgets.QSpinBox.CorrectionMode] = bidict(
    to_previous=QtWidgets.QSpinBox.CorrectionMode.CorrectToPreviousValue,
    to_nearest=QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue,
)

SymbolStr = Literal["up_down", "plus_minus", "none"]

SYMBOLS: bidict[SymbolStr, QtWidgets.QSpinBox.ButtonSymbols] = bidict(
    up_down=QtWidgets.QSpinBox.ButtonSymbols.UpDownArrows,
    plus_minus=QtWidgets.QSpinBox.ButtonSymbols.PlusMinus,
    none=QtWidgets.QSpinBox.ButtonSymbols.NoButtons,
)

StepTypeStr = Literal["default", "adaptive"]

STEP_TYPES: bidict[StepTypeStr, QtWidgets.QSpinBox.StepType] = bidict(
    default=QtWidgets.QSpinBox.StepType.DefaultStepType,
    adaptive=QtWidgets.QSpinBox.StepType.AdaptiveDecimalStepType,
)

StepEnabledFlagStr = Literal["none", "up_enabled", "down_enabled"]

STEP_ENABLED_FLAG: bidict[
    StepEnabledFlagStr, QtWidgets.QSpinBox.StepEnabledFlag
] = bidict(
    none=QtWidgets.QSpinBox.StepEnabledFlag.StepNone,
    up_enabled=QtWidgets.QSpinBox.StepEnabledFlag.StepUpEnabled,
    down_enabled=QtWidgets.QSpinBox.StepEnabledFlag.StepDownEnabled,
)


class AbstractSpinBoxMixin(widgets.WidgetMixin):
    def __init__(self, *args, show_group_separator: bool = True, **kwargs):
        super().__init__(*args, show_group_separator=show_group_separator, **kwargs)
        self.setLineEdit(widgets.LineEdit(parent=self))

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "alignment": constants.ALIGNMENTS,
            "buttonSymbols": SYMBOLS,
            "correctionMode": CORRECTION_MODES,
        }
        return maps

    def is_valid(self) -> bool:
        return self.hasAcceptableInput()

    def set_validator(
        self, validator: QtGui.QValidator | widgets.lineedit.ValidatorStr | None, **kwargs
    ) -> QtGui.QValidator:
        return self.lineEdit().set_validator(validator)

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

    def set_value(self, value: int | float):
        self.setValue(value)


class AbstractSpinBox(AbstractSpinBoxMixin, QtWidgets.QAbstractSpinBox):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = AbstractSpinBox()
    widget.show()
    app.exec()
