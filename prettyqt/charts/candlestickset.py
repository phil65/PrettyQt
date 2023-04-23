from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import QtCharts
from prettyqt.utils import get_repr


class CandlestickSet(core.ObjectMixin, QtCharts.QCandlestickSet):
    def __repr__(self):
        return get_repr(
            self, self.open(), self.high(), self.low(), self.close(), self.timestamp()
        )

    def get_pen(self) -> gui.Pen:
        return gui.Pen(self.pen())

    def get_brush(self) -> gui.Brush:
        return gui.Brush(self.brush())


if __name__ == "__main__":
    candlestickset = CandlestickSet(1, 3, 0, 2)
    print(repr(candlestickset))
