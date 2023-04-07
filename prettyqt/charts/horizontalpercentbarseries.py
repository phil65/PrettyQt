from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class HorizontalPercentBarSeries(
    charts.AbstractBarSeriesMixin, QtCharts.QHorizontalPercentBarSeries
):
    pass
