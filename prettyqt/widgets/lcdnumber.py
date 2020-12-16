from typing import Literal, Union

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict


MODE = bidict(
    hex=QtWidgets.QLCDNumber.Hex,
    decimal=QtWidgets.QLCDNumber.Dec,
    octal=QtWidgets.QLCDNumber.Oct,
    binary=QtWidgets.QLCDNumber.Bin,
)

ModeStr = Literal["hex", "decimal", "octal", "binary"]

SEGMENT_STYLE = bidict(
    outline=QtWidgets.QLCDNumber.Outline,
    filled=QtWidgets.QLCDNumber.Filled,
    flat=QtWidgets.QLCDNumber.Flat,
)

SegmentStyleStr = Literal["outline", "filled", "flat"]

QtWidgets.QLCDNumber.__bases__ = (widgets.Frame,)


class LCDNumber(QtWidgets.QLCDNumber):
    def set_mode(self, mode: ModeStr):
        """Set the lcd mode.

        Args:
            mode: lcd mode to use

        Raises:
            InvalidParamError: lcd mode does not exist
        """
        if mode not in MODE:
            raise InvalidParamError(mode, MODE)
        self.setMode(MODE[mode])

    def get_mode(self) -> ModeStr:
        """Return current lcd mode.

        Returns:
            lcd mode
        """
        return MODE.inverse[self.mode()]

    def set_segment_style(self, mode: SegmentStyleStr):
        """Set the segment style.

        Args:
            mode: segment style to use

        Raises:
            InvalidParamError: segment style does not exist
        """
        if mode not in SEGMENT_STYLE:
            raise InvalidParamError(mode, SEGMENT_STYLE)
        self.setSegmentStyle(SEGMENT_STYLE[mode])

    def get_segment_style(self) -> SegmentStyleStr:
        """Return current segment style.

        Returns:
            segment style
        """
        return SEGMENT_STYLE.inverse[self.segmentStyle()]

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
