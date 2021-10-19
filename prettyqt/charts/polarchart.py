from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.qt import QtCharts
from prettyqt.utils import InvalidParamError, bidict


POLAR_ORIENTATIONS = bidict(
    radial=QtCharts.QPolarChart.PolarOrientation.PolarOrientationRadial,
    angular=QtCharts.QPolarChart.PolarOrientation.PolarOrientationAngular,
)

PolarOrientationStr = Literal["radial", "angular"]

QtCharts.QPolarChart.__bases__ = (charts.Chart,)


class PolarChart(QtCharts.QPolarChart):
    def add_axis(self, axis: QtCharts.QAbstractAxis, orientation: PolarOrientationStr):
        if orientation not in POLAR_ORIENTATIONS:
            raise InvalidParamError(orientation, POLAR_ORIENTATIONS)
        self.addAxis(axis, POLAR_ORIENTATIONS[orientation])
