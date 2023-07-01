from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCharts
from prettyqt.utils import bidict, get_repr


LabelPositionStr = Literal[
    "outside", "inside_horizontal", "inside_tangential", "inside_normal"
]


LABEL_POSITION: bidict[LabelPositionStr, QtCharts.QPieSlice.LabelPosition] = bidict(
    outside=QtCharts.QPieSlice.LabelPosition.LabelOutside,
    inside_horizontal=QtCharts.QPieSlice.LabelPosition.LabelInsideHorizontal,
    inside_tangential=QtCharts.QPieSlice.LabelPosition.LabelInsideTangential,
    inside_normal=QtCharts.QPieSlice.LabelPosition.LabelInsideNormal,
)


class PieSlice(core.ObjectMixin, QtCharts.QPieSlice):
    def __repr__(self):
        return get_repr(self, self.label(), self.value())

    def set_label_position(self, position: LabelPositionStr):
        """Set the label position.

        Args:
            position: label position
        """
        self.setLabelPosition(LABEL_POSITION.get_enum_value(position))

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
