from __future__ import annotations

from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


LabelsPositionStr = Literal["center", "inside_end", "inside_base", "outside_end"]

LABELS_POSITIONS: bidict[
    LabelsPositionStr, charts.QAbstractBarSeries.LabelsPosition
] = bidict(
    center=charts.QAbstractBarSeries.LabelsPosition.LabelsCenter,
    inside_end=charts.QAbstractBarSeries.LabelsPosition.LabelsInsideEnd,
    inside_base=charts.QAbstractBarSeries.LabelsPosition.LabelsInsideBase,
    outside_end=charts.QAbstractBarSeries.LabelsPosition.LabelsOutsideEnd,
)


class AbstractBarSeriesMixin(charts.AbstractSeriesMixin):
    def __delitem__(self, item: int | charts.QBarSet):
        """Implements `del series[0]`."""
        if isinstance(item, int):
            barsets = self.barSets()
            item = barsets[item]
        self.remove(item)

    def __getitem__(self, index: int) -> charts.QBarSet:
        """Implements `barset = series[1]`."""
        barsets = self.barSets()
        return barsets[index]

    def set_labels_position(
        self, position: LabelsPositionStr | charts.QAbstractBarSeries.LabelsPosition
    ):
        """Set the labels position.

        Args:
            position: labels position
        """
        self.setLabelsPosition(LABELS_POSITIONS.get_enum_value(position))

    def get_labels_position(self) -> LabelsPositionStr:
        """Return current labels position.

        Returns:
            labels position
        """
        return LABELS_POSITIONS.inverse[self.labelsPosition()]


class AbstractBarSeries(AbstractBarSeriesMixin, charts.QAbstractBarSeries):
    pass
