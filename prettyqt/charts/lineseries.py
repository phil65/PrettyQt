from qtpy import QtCore
from qtpy.QtCharts import QtCharts

from prettyqt import charts, core


QtCharts.QLineSeries.__bases__ = (charts.XYSeries,)


class LineSeries(QtCharts.QLineSeries):
    """QLineSeries with some custom properties."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._process_name = ""

    def get_process_name(self):
        return self._process_name

    def set_process_name(self, value):
        self._process_name = value

    process_name = core.Property(str, get_process_name, set_process_name)


if __name__ == "__main__":
    line = LineSeries()
    line += QtCore.QPointF(1, 1)
