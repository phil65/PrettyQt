from __future__ import annotations

from prettyqt import charts


class LineSeries(charts.XYSeriesMixin, charts.QLineSeries):
    """QLineSeries with some custom properties."""


if __name__ == "__main__":
    from prettyqt.qt import QtCore

    line = LineSeries()
    line += QtCore.QPointF(1, 1)
