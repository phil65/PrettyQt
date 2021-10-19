from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCharts


QtCharts.QBarSet.__bases__ = (core.Object,)


class BarSet(QtCharts.QBarSet):
    def __delitem__(self, index: int):
        if not (0 <= index < self.count()):
            raise KeyError(index)
        self.remove(index)

    def __getitem__(self, index: int) -> float:
        if not (0 <= index < self.count()):
            raise KeyError(index)
        return self.at(index)

    def __setitem__(self, index: int, value: float):
        if not (0 <= index < self.count()):
            raise KeyError(index)
        self.replace(index, value)

    def __repr__(self):
        return f"{type(self).__name__}({self.label()!r})"

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    barset = BarSet("test")
    print(repr(barset))
