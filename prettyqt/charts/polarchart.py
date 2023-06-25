from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.qt import QtCharts
from prettyqt.utils import bidict


POLAR_ORIENTATIONS = bidict(
    radial=QtCharts.QPolarChart.PolarOrientation.PolarOrientationRadial,
    angular=QtCharts.QPolarChart.PolarOrientation.PolarOrientationAngular,
)

PolarOrientationStr = Literal["radial", "angular"]


class PolarChart(charts.ChartMixin, QtCharts.QPolarChart):
    def add_axis(
        self,
        axis: QtCharts.QAbstractAxis,
        orientation: PolarOrientationStr | QtCharts.QPolarChart.PolarOrientation,
    ):
        self.addAxis(axis, POLAR_ORIENTATIONS[orientation])
