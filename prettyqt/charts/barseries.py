from prettyqt import charts
from prettyqt.qt.QtCharts import QtCharts


QtCharts.QBarSeries.__bases__ = (charts.AbstractBarSeries,)


class BarSeries(QtCharts.QBarSeries):
    pass
