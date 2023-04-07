from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class HorizontalStackedBarSeries(
    charts.AbstractBarSeriesMixin, QtCharts.QHorizontalStackedBarSeries
):
    pass
