from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.qt import QtCharts
from prettyqt.utils import InvalidParamError, bidict


LABELS_POSITIONS = bidict(
    center=QtCharts.QAbstractBarSeries.LabelsPosition.LabelsCenter,
    inside_end=QtCharts.QAbstractBarSeries.LabelsPosition.LabelsInsideEnd,
    inside_base=QtCharts.QAbstractBarSeries.LabelsPosition.LabelsInsideBase,
    outside_end=QtCharts.QAbstractBarSeries.LabelsPosition.LabelsOutsideEnd,
)

LabelsPositionStr = Literal["center", "inside_end", "inside_base", "outside_end"]

QtCharts.QAbstractBarSeries.__bases__ = (charts.AbstractSeries,)


class AbstractBarSeries(QtCharts.QAbstractBarSeries):
    def __delitem__(self, index: int):
        barsets = self.barSets()
        self.remove(barsets[index])

    def __getitem__(self, index: int) -> QtCharts.QBarSet:
        barsets = self.barSets()
        return barsets[index]

    def set_labels_position(self, position: LabelsPositionStr):
        """Set the labels position.

        Args:
            position: labels position

        Raises:
            InvalidParamError: labels position does not exist
        """
        if position not in LABELS_POSITIONS:
            raise InvalidParamError(position, LABELS_POSITIONS)
        self.setLabelsPosition(LABELS_POSITIONS[position])

    def get_labels_position(self) -> LabelsPositionStr:
        """Return current labels position.

        Returns:
            labels position
        """
        return LABELS_POSITIONS.inverse[self.labelsPosition()]
