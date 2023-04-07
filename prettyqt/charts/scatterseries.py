from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class ScatterSeries(charts.XYSeriesMixin, QtCharts.QScatterSeries):
    pass
