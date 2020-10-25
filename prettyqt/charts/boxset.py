# -*- coding: utf-8 -*-

from typing import Union

from qtpy.QtCharts import QtCharts

from prettyqt import core, gui
from prettyqt.utils import bidict


VALUE_POSITIONS = bidict(
    lower_extreme=QtCharts.QBoxSet.LowerExtreme,
    lower_quartile=QtCharts.QBoxSet.LowerQuartile,
    median=QtCharts.QBoxSet.Median,
    upper_quartile=QtCharts.QBoxSet.UpperQuartile,
    upper_extreme=QtCharts.QBoxSet.UpperExtreme,
)


QtCharts.QBoxSet.__bases__ = (core.Object,)


class BoxSet(QtCharts.QBoxSet):
    def __repr__(self):
        return (
            f"BoxSet({self['lower_extreme']}, {self['lower_quartile']}, {self['median']},"
            f" {self['upper_quartile']}, {self['upper_extreme']}, {self.label()!r})"
        )

    def __getitem__(self, index: Union[int, str]) -> float:
        if index in VALUE_POSITIONS:
            index = VALUE_POSITIONS[index]
        return self.at(index)

    def __setitem__(self, index: Union[int, str], value: int):
        if index in VALUE_POSITIONS:
            index = VALUE_POSITIONS[index]
        self.setValue(index, value)

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    boxset = BoxSet()
    print(repr(boxset))
