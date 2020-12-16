from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import InvalidParamError, bidict


POLAR_ORIENTATIONS = bidict(
    radial=QtCharts.QPolarChart.PolarOrientationRadial,
    angular=QtCharts.QPolarChart.PolarOrientationAngular,
)


QtCharts.QPolarChart.__bases__ = (charts.Chart,)


class PolarChart(QtCharts.QPolarChart):
    def add_axis(self, axis: QtCharts.QAbstractAxis, orientation: str):
        if orientation not in POLAR_ORIENTATIONS:
            raise InvalidParamError(orientation, POLAR_ORIENTATIONS)
        self.addAxis(axis, POLAR_ORIENTATIONS[orientation])
