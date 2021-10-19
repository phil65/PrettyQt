from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QHorizontalBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalBarSeries(QtCharts.QHorizontalBarSeries):
    pass
