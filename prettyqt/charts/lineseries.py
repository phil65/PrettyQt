# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore
from qtpy.QtCharts import QtCharts
from prettyqt import core, charts

STYLES = {QtCore.Qt.SolidLine: "Solid",
          QtCore.Qt.DotLine: "Dot",
          QtCore.Qt.DashDotLine: "Dash-dot"}


QtCharts.QLineSeries.__bases__ = (charts.XYSeries,)


class LineSeries(QtCharts.QLineSeries):

    """
    QLineSeries with some custom properties
    """

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
    line.append(0, 1)
