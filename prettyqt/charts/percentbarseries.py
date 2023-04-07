from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class PercentBarSeries(charts.AbstractBarSeriesMixin, QtCharts.QPercentBarSeries):
    pass
