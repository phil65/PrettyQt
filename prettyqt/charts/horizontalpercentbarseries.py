from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QHorizontalPercentBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalPercentBarSeries(QtCharts.QHorizontalPercentBarSeries):
    pass
