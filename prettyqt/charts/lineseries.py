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

    def __getstate__(self):
        return dict(points=self.pointsVector())

    def __setstate__(self, state):
        super().__init__()
        super().append(state["points"])
        pass


if __name__ == "__main__":
    line = LineSeries()
    line.append(0, 1)
