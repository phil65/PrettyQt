from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QHorizontalStackedBarSeries.__bases__ = (charts.AbstractBarSeries,)


class HorizontalStackedBarSeries(QtCharts.QHorizontalStackedBarSeries):
    pass
