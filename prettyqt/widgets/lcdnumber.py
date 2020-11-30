# -*- coding: utf-8 -*-

from typing import Union

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError

MODE = bidict(
    hex=QtWidgets.QLCDNumber.Hex,
    decimal=QtWidgets.QLCDNumber.Dec,
    octal=QtWidgets.QLCDNumber.Oct,
    binary=QtWidgets.QLCDNumber.Bin,
)

SEGMENT_STYLE = bidict(
    outline=QtWidgets.QLCDNumber.Outline,
    filled=QtWidgets.QLCDNumber.Filled,
    flat=QtWidgets.QLCDNumber.Flat,
)

QtWidgets.QLCDNumber.__bases__ = (widgets.Widget,)


class LCDNumber(QtWidgets.QLCDNumber):
    def set_mode(self, mode: str):
        """Set the lcd mode.

        Allowed values are "hex", "decimal", "octal", "binary"

        Args:
            mode: lcd mode to use

        Raises:
            InvalidParamError: lcd mode does not exist
        """
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        self.setMode(MODE[mode])

    def get_mode(self) -> str:
        """Return current lcd mode.

        Possible values: "hex", "decimal", "octal", "binary"

        Returns:
            lcd mode
        """
        return MODE.inv[self.mode()]

    def set_segment_style(self, mode: str):
        """Set the segment style.

        Allowed values are "outline", "filled", "flat"

        Args:
            mode: segment style to use

        Raises:
            InvalidParamError: segment style does not exist
        """
        if mode not in SEGMENT_STYLE:
            raise InvalidParamError(mode, SEGMENT_STYLE)
        self.setSegmentStyle(SEGMENT_STYLE[mode])

    def get_segment_style(self) -> str:
        """Return current segment style.

        Possible values: "outline", "filled", "flat"

        Returns:
            segment style
        """
        return SEGMENT_STYLE.inv[self.segmentStyle()]

    def set_value(self, value: Union[float, str]):
        self.display(value)

    def get_value(self) -> float:
        return self.value()


if __name__ == "__main__":
    app = widgets.app()
    widget = LCDNumber()
    widget.set_value(5555)
    widget.show()
    app.main_loop()
