from __future__ import annotations

from typing import Literal, Union

from prettyqt import core, gui
from prettyqt.qt.QtCharts import QtCharts
from prettyqt.utils import bidict


VALUE_POSITION = bidict(
    lower_extreme=QtCharts.QBoxSet.LowerExtreme,
    lower_quartile=QtCharts.QBoxSet.LowerQuartile,
    median=QtCharts.QBoxSet.Median,
    upper_quartile=QtCharts.QBoxSet.UpperQuartile,
    upper_extreme=QtCharts.QBoxSet.UpperExtreme,
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

    def __getitem__(self, index: Union[int, ValuePositionStr]) -> float:
        if isinstance(index, str):
            index = VALUE_POSITION[index]
        elif not (0 <= index <= 4):
            raise KeyError(index)
        return self.at(index)

    def __setitem__(self, index: Union[int, ValuePositionStr], value: int):
        if isinstance(index, str):
            index = VALUE_POSITION[index]
        elif not (0 <= index <= 4):
            raise KeyError(index)
        self.setValue(index, value)

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    boxset = BoxSet()
    print(repr(boxset))
