from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import bidict, InvalidParamError


LABELS_POSITIONS = bidict(
    center=QtCharts.QAbstractBarSeries.LabelsCenter,
    inside_end=QtCharts.QAbstractBarSeries.LabelsInsideEnd,
    inside_base=QtCharts.QAbstractBarSeries.LabelsInsideBase,
    outside_end=QtCharts.QAbstractBarSeries.LabelsOutsideEnd,
)


QtCharts.QAbstractBarSeries.__bases__ = (charts.AbstractSeries,)


class AbstractBarSeries(QtCharts.QAbstractBarSeries):
    def __delitem__(self, index: int):
        barsets = self.barSets()
        self.remove(barsets[index])

    def __getitem__(self, index: int) -> QtCharts.QBarSet:
        barsets = self.barSets()
        return barsets[index]

    def set_labels_position(self, position: str):
        """Set the labels position.

        Allowed values are "center", "inside_end", "inside_base", "outside_end"

        Args:
            position: labels position

        Raises:
            InvalidParamError: labels position does not exist
        """
        if position not in LABELS_POSITIONS:
            raise InvalidParamError(position, LABELS_POSITIONS)
        self.setLabelsPosition(LABELS_POSITIONS[position])

    def get_labels_position(self) -> str:
        """Return current labels position.

        Possible values: "center", "inside_end", "inside_base", "outside_end"

        Returns:
            labels position
        """
        return LABELS_POSITIONS.inverse[self.labelsPosition()]
