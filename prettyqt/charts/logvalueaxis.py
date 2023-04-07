from __future__ import annotations

from prettyqt import charts
from prettyqt.qt import QtCharts


class LogValueAxis(charts.AbstractAxisMixin, QtCharts.QLogValueAxis):
    pass
