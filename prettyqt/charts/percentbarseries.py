from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QPercentBarSeries.__bases__ = (charts.AbstractBarSeries,)


class PercentBarSeries(QtCharts.QPercentBarSeries):
    pass
