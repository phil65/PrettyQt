from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QBarSeries.__bases__ = (charts.AbstractBarSeries,)


class BarSeries(QtCharts.QBarSeries):
    pass
