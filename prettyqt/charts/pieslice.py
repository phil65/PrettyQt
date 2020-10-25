# -*- coding: utf-8 -*-

from qtpy.QtCharts import QtCharts

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError


LABEL_POSITIONS = bidict(
    outside=QtCharts.QPieSlice.LabelOutside,
    inside_horizontal=QtCharts.QPieSlice.LabelInsideHorizontal,
    inside_tangential=QtCharts.QPieSlice.LabelInsideTangential,
    inside_normal=QtCharts.QPieSlice.LabelInsideNormal,
)


QtCharts.QPieSlice.__bases__ = (core.Object,)


class PieSlice(QtCharts.QPieSlice):
    def __repr__(self):
        return f"PieSlice({self.label()!r}, {self.value()})"

    def set_label_position(self, position: str):
        """Set the label position.

        Allowed values are "outside", "inside_horizontal", "inside_tangential",
        "inside_normal"

        Args:
            position: label position

        Raises:
            InvalidParamError: label position does not exist
        """
        if position not in LABEL_POSITIONS:
            raise InvalidParamError(position, LABEL_POSITIONS)
        self.setLabelPosition(LABEL_POSITIONS[position])

    def get_label_position(self) -> str:
        """Return current label position.

        Possible values: "outside", "inside_horizontal", "inside_tangential",
        "inside_normal"

        Returns:
            label position
        """
        return LABEL_POSITIONS.inv[self.labelPosition()]

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
