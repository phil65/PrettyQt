# -*- coding: utf-8 -*-

from qtpy.QtCharts import QtCharts

from prettyqt import core, gui


QtCharts.QBarSet.__bases__ = (core.Object,)


class BarSet(QtCharts.QBarSet):
    def __delitem__(self, index: int):
        self.remove(index)

    def __getitem__(self, label: int) -> float:
        return self.at(label)

    def __setitem__(self, index: int, value: float):
        self.replace(index, value)

    def __repr__(self):
        return f"BarSet({self.label()!r})"

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    candlestickset = BarSet(1, 3, 0, 2)
    print(repr(candlestickset))
