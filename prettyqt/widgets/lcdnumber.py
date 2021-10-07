from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


MODE = bidict(
    hex=QtWidgets.QLCDNumber.Mode.Hex,
    decimal=QtWidgets.QLCDNumber.Mode.Dec,
    octal=QtWidgets.QLCDNumber.Mode.Oct,
    binary=QtWidgets.QLCDNumber.Mode.Bin,
)

ModeStr = Literal["hex", "decimal", "octal", "binary"]

SEGMENT_STYLE = bidict(
    outline=QtWidgets.QLCDNumber.SegmentStyle.Outline,
    filled=QtWidgets.QLCDNumber.SegmentStyle.Filled,
    flat=QtWidgets.QLCDNumber.SegmentStyle.Flat,
)

SegmentStyleStr = Literal["outline", "filled", "flat"]

QtWidgets.QLCDNumber.__bases__ = (widgets.Frame,)


class LCDNumber(QtWidgets.QLCDNumber):
    def serialize_fields(self):
        return dict(
            mode=self.get_mode(),
            segment_style=self.get_segment_style(),
            value=self.get_value(),
        )

    def __setstate__(self, state):
        self.set_mode(state["mode"])
        self.set_segment_style(state["segment_style"])
        self.set_value(state["value"])

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

    def set_value(self, value: float | str):
        self.display(value)

    def get_value(self) -> float:
        return self.value()


if __name__ == "__main__":
    app = widgets.app()
    widget = LCDNumber()
    widget.set_value(5555)
    widget.show()
    app.main_loop()
