from qtpy.QtCharts import QtCharts

from prettyqt import charts


QtCharts.QLogValueAxis.__bases__ = (charts.AbstractAxis,)


class LogValueAxis(QtCharts.QLogValueAxis):
    pass
