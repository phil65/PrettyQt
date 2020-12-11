from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QHorizontalBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalBarSeries(QtCharts.QHorizontalBarSeries):
    pass
