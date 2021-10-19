from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QPercentBarSeries.__bases__ = (charts.AbstractBarSeries,)


class PercentBarSeries(QtCharts.QPercentBarSeries):
    pass
