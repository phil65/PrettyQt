import datetime

from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import to_datetime


QtCharts.QDateTimeAxis.__bases__ = (charts.AbstractAxis,)


class DateTimeAxis(QtCharts.QDateTimeAxis):
    def get_min(self) -> datetime.datetime:
        return to_datetime(self.min())

    def get_max(self) -> datetime.datetime:
        return to_datetime(self.max())
