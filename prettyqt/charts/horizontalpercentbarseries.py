from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QHorizontalPercentBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalPercentBarSeries(QtCharts.QHorizontalPercentBarSeries):
    pass
