from __future__ import annotations

from prettyqt import charts
from prettyqt.qt.QtCharts import QtCharts


QtCharts.QScatterSeries.__bases__ = (charts.XYSeries,)


class ScatterSeries(QtCharts.QScatterSeries):
    pass
