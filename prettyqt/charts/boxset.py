from __future__ import annotations

from typing import Literal

from prettyqt import core, gui
from prettyqt.qt import QtCharts
from prettyqt.utils import bidict, get_repr


ValuePositionStr = Literal[
    "lower_extreme", "lower_quartile", "median", "upper_quartile", "upper_extreme"
]

VALUE_POSITION: bidict[ValuePositionStr, QtCharts.QBoxSet.ValuePositions] = bidict(
    lower_extreme=QtCharts.QBoxSet.ValuePositions.LowerExtreme,
    lower_quartile=QtCharts.QBoxSet.ValuePositions.LowerQuartile,
    median=QtCharts.QBoxSet.ValuePositions.Median,
    upper_quartile=QtCharts.QBoxSet.ValuePositions.UpperQuartile,
    upper_extreme=QtCharts.QBoxSet.ValuePositions.UpperExtreme,
)


class BoxSet(core.ObjectMixin, QtCharts.QBoxSet):
    def __repr__(self):
        return get_repr(
            self,
            self["lower_extreme"],
            self["lower_quartile"],
            self["median"],
            self["upper_quartile"],
            self["upper_extreme"],
            self.label(),
        )

    def __getitem__(
        self, index: int | ValuePositionStr | QtCharts.QBoxSet.ValuePositions
    ) -> float:
        """Returns the value of the box-and-whiskers item specified by index."""
        if type(index) is not int:
            index = VALUE_POSITION.get_enum_value(index).value
        if not (0 <= index <= 4):  # noqa: PLR2004
            raise KeyError(index)
        return self.at(index)

    def __setitem__(
        self, index: int | ValuePositionStr | QtCharts.QBoxSet.ValuePositions, value: int
    ):
        """Sets the value specified by value in the position specified by index."""
        if type(index) is not int:
            index = VALUE_POSITION.get_enum_value(index).value
        if not (0 <= index <= 4):  # noqa: PLR2004
            raise KeyError(index)
        self.setValue(index, value)

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    boxset = BoxSet()
    boxset[0]
