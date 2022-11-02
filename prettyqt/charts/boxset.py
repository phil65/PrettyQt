from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, qt
from prettyqt.qt import QtCharts
from prettyqt.utils import bidict


VALUE_POSITION = bidict(
    lower_extreme=QtCharts.QBoxSet.ValuePositions.LowerExtreme,
    lower_quartile=QtCharts.QBoxSet.ValuePositions.LowerQuartile,
    median=QtCharts.QBoxSet.ValuePositions.Median,
    upper_quartile=QtCharts.QBoxSet.ValuePositions.UpperQuartile,
    upper_extreme=QtCharts.QBoxSet.ValuePositions.UpperExtreme,
)

ValuePositionStr = Literal[
    "lower_extreme", "lower_quartile", "median", "upper_quartile", "upper_extreme"
]

QtCharts.QBoxSet.__bases__ = (core.Object,)


class BoxSet(QtCharts.QBoxSet):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self['lower_extreme']}, {self['lower_quartile']},"
            f" {self['median']}, {self['upper_quartile']}, {self['upper_extreme']}, "
            f"{self.label()!r})"
        )

    def __getitem__(self, index: int | ValuePositionStr) -> float:
        val = VALUE_POSITION[index] if isinstance(index, str) else index
        if not (0 <= qt.flag_to_int(val) <= 4):
            raise KeyError(val)
        return self.at(qt.flag_to_int(val))

    def __setitem__(self, index: int | ValuePositionStr, value: int):
        val = VALUE_POSITION[index] if isinstance(index, str) else index
        if not (0 <= qt.flag_to_int(val) <= 4):
            raise KeyError(val)
        self.setValue(qt.flag_to_int(val), value)

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    boxset = BoxSet()
    print(repr(boxset))
