from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QHorizontalStackedBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalStackedBarSeries(QtCharts.QHorizontalStackedBarSeries):
    pass
