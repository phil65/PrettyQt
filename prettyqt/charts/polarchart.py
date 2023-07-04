from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


PolarOrientationStr = Literal["radial", "angular"]

POLAR_ORIENTATIONS: bidict[
    PolarOrientationStr, charts.QPolarChart.PolarOrientation
] = bidict(
    radial=charts.QPolarChart.PolarOrientation.PolarOrientationRadial,
    angular=charts.QPolarChart.PolarOrientation.PolarOrientationAngular,
)


class PolarChart(charts.ChartMixin, charts.QPolarChart):
    def add_axis(
        self,
        axis: charts.QAbstractAxis,
        orientation: PolarOrientationStr | charts.QPolarChart.PolarOrientation,
    ):
        """Add axis with given orientation."""
        self.addAxis(axis, POLAR_ORIENTATIONS.get_enum_value(orientation))
