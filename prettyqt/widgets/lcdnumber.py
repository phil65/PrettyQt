from __future__ import annotations

from typing import Literal

from prettyqt import core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


ModeStr = Literal["hex", "decimal", "octal", "binary"]

MODE: bidict[ModeStr, QtWidgets.QLCDNumber.Mode] = bidict(
    hex=QtWidgets.QLCDNumber.Mode.Hex,
    decimal=QtWidgets.QLCDNumber.Mode.Dec,
    octal=QtWidgets.QLCDNumber.Mode.Oct,
    binary=QtWidgets.QLCDNumber.Mode.Bin,
)

SegmentStyleStr = Literal["outline", "filled", "flat"]

SEGMENT_STYLE: bidict[SegmentStyleStr, QtWidgets.QLCDNumber.SegmentStyle] = bidict(
    outline=QtWidgets.QLCDNumber.SegmentStyle.Outline,
    filled=QtWidgets.QLCDNumber.SegmentStyle.Filled,
    flat=QtWidgets.QLCDNumber.SegmentStyle.Flat,
)


class LCDNumber(widgets.FrameMixin, QtWidgets.QLCDNumber):
    value_changed = core.Signal(float)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"segmentStyle": SEGMENT_STYLE, "mode": MODE}
        return maps

    def set_mode(self, mode: ModeStr | QtWidgets.QLCDNumber.Mode):
        """Set the lcd mode.

        Args:
            mode: lcd mode to use
        """
        self.setMode(MODE.get_enum_value(mode))

    def get_mode(self) -> ModeStr:
        """Return current lcd mode.

        Returns:
            lcd mode
        """
        return MODE.inverse[self.mode()]

    def set_segment_style(
        self, style: SegmentStyleStr | QtWidgets.QLCDNumber.SegmentStyle
    ):
        """Set the segment style.

        Args:
            style: segment style to use
        """
        self.setSegmentStyle(SEGMENT_STYLE.get_enum_value(style))

    def get_segment_style(self) -> SegmentStyleStr:
        """Return current segment style.

        Returns:
            segment style
        """
        return SEGMENT_STYLE.inverse[self.segmentStyle()]

    def set_value(self, value: float | str):
        if value != self.value():
            self.value_changed.emit(float(value))
        self.display(value)

    def get_value(self) -> float:
        return self.value()


if __name__ == "__main__":
    app = widgets.app()
    widget = LCDNumber()
    widget.set_value(5555)
    widget.show()
    app.exec()
