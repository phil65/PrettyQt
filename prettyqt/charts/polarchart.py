from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


POLAR_ORIENTATIONS = bidict(
    radial=charts.QPolarChart.PolarOrientation.PolarOrientationRadial,
    angular=charts.QPolarChart.PolarOrientation.PolarOrientationAngular,
)

PolarOrientationStr = Literal["radial", "angular"]


class PolarChart(charts.ChartMixin, charts.QPolarChart):
    def add_axis(
        self,
        axis: charts.QAbstractAxis,
        orientation: PolarOrientationStr | charts.QPolarChart.PolarOrientation,
    ):
        self.addAxis(axis, POLAR_ORIENTATIONS[orientation])
