from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QBarSeries.__bases__ = (charts.AbstractBarSeries,)


class BarSeries(QtCharts.QBarSeries):
    pass
