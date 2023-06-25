from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts, QtCore


class LineSeries(charts.XYSeriesMixin, QtCharts.QLineSeries):
    """QLineSeries with some custom properties."""
    pass

if __name__ == "__main__":
    line = LineSeries()
    line += QtCore.QPointF(1, 1)
