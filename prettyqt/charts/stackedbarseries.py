from __future__ import annotations

from prettyqt import charts
from prettyqt.qt.QtCharts import QtCharts


QtCharts.QStackedBarSeries.__bases__ = (charts.AbstractBarSeries,)


class StackedBarSeries(QtCharts.QStackedBarSeries):
    pass
