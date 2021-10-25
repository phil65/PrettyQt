from __future__ import annotations

import datetime

from prettyqt import charts
from prettyqt.qt import QtCharts


QtCharts.QDateTimeAxis.__bases__ = (charts.AbstractAxis,)


class DateTimeAxis(QtCharts.QDateTimeAxis):
    def get_min(self) -> datetime.datetime:
        return self.min().toPython()  # type: ignore

    def get_max(self) -> datetime.datetime:
        return self.max().toPython()  # type: ignore
