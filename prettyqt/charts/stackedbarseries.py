from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QStackedBarSeries.__bases__ = (charts.AbstractBarSeries,)


class StackedBarSeries(QtCharts.QStackedBarSeries):
    pass
