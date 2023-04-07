from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class StackedBarSeries(charts.AbstractBarSeriesMixin, QtCharts.QStackedBarSeries):
    pass
