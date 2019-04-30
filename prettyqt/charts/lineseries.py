# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy.QtCharts import QtCharts
from qtpy import QtCore

STYLES = {QtCore.Qt.SolidLine: "Solid",
          QtCore.Qt.DotLine: "Dot",
          QtCore.Qt.DashDotLine: "Dash-dot"}


class LineSeries(QtCharts.QLineSeries):
    pass
