from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCharts
from prettyqt.utils import InvalidParamError, bidict


LABEL_POSITION = bidict(
    outside=QtCharts.QPieSlice.LabelPosition.LabelOutside,
    inside_horizontal=QtCharts.QPieSlice.LabelPosition.LabelInsideHorizontal,
    inside_tangential=QtCharts.QPieSlice.LabelPosition.LabelInsideTangential,
    inside_normal=QtCharts.QPieSlice.LabelPosition.LabelInsideNormal,
)

LabelPositionStr = Literal[
    "outside", "inside_horizontal", "inside_tangential", "inside_normal"
]

QtCharts.QPieSlice.__bases__ = (core.Object,)


class PieSlice(QtCharts.QPieSlice):
    def __repr__(self):
        return f"{type(self).__name__}({self.label()!r}, {self.value()})"

    def set_label_position(self, position: LabelPositionStr):
        """Set the label position.

        Args:
            position: label position

        Raises:
            InvalidParamError: label position does not exist
        """
        if position not in LABEL_POSITION:
            raise InvalidParamError(position, LABEL_POSITION)
        self.setLabelPosition(LABEL_POSITION[position])

    def get_label_position(self) -> LabelPositionStr:
        """Return current label position.

        Returns:
            label position
        """
        return LABEL_POSITION.inverse[self.labelPosition()]

    def get_label_font(self) -> gui.Font:
        return gui.Font(self.labelFont())

    def get_label_brush(self) -> gui.Brush:
        return gui.Brush(self.labelBrush())

    def get_label_color(self) -> gui.Color:
        return gui.Color(self.labelColor())

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())

    def get_color(self) -> gui.Color:
        return gui.Color(self.color())

    def get_border_color(self) -> gui.Color:
        return gui.Color(self.borderColor())


if __name__ == "__main__":
    pieslice = PieSlice("test", 1)
    print(repr(pieslice))
