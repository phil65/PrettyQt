from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class BarSeries(charts.AbstractBarSeriesMixin, QtCharts.QBarSeries):
    pass
