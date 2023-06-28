from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


LABELS_POSITIONS = bidict(
    center=charts.QAbstractBarSeries.LabelsPosition.LabelsCenter,
    inside_end=charts.QAbstractBarSeries.LabelsPosition.LabelsInsideEnd,
    inside_base=charts.QAbstractBarSeries.LabelsPosition.LabelsInsideBase,
    outside_end=charts.QAbstractBarSeries.LabelsPosition.LabelsOutsideEnd,
)

LabelsPositionStr = Literal["center", "inside_end", "inside_base", "outside_end"]


class AbstractBarSeriesMixin(charts.AbstractSeriesMixin):
    def __delitem__(self, item: int | charts.QBarSet):
        if isinstance(item, int):
            barsets = self.barSets()
            item = barsets[item]
        self.remove(item)

    def __getitem__(self, index: int) -> charts.QBarSet:
        barsets = self.barSets()
        return barsets[index]

    def set_labels_position(
        self, position: LabelsPositionStr | charts.QAbstractBarSeries.LabelsPosition
    ):
        """Set the labels position.

        Args:
            position: labels position
        """
        self.setLabelsPosition(LABELS_POSITIONS[position])

    def get_labels_position(self) -> LabelsPositionStr:
        """Return current labels position.

        Returns:
            labels position
        """
        return LABELS_POSITIONS.inverse[self.labelsPosition()]


class AbstractBarSeries(AbstractBarSeriesMixin, charts.QAbstractBarSeries):
    pass
