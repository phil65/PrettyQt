from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QLogValueAxis.__bases__ = (charts.AbstractAxis,)


class LogValueAxis(QtCharts.QLogValueAxis):
    pass
