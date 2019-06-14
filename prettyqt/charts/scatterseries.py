# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy.QtCharts import QtCharts
from prettyqt import charts


QtCharts.QScatterSeries.__bases__ = (charts.XYSeries,)


class ScatterSeries(QtCharts.QScatterSeries):
    pass
