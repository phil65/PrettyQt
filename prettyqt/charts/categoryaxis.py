from __future__ import annotations

from typing import Tuple, Iterator

from qtpy.QtCharts import QtCharts

from prettyqt import charts
from prettyqt.utils import bidict, InvalidParamError

LABELS_POSITIONS = bidict(
    center=QtCharts.QCategoryAxis.AxisLabelsPositionCenter,
    on_value=QtCharts.QCategoryAxis.AxisLabelsPositionOnValue,
)

QtCharts.QCategoryAxis.__bases__ = (charts.ValueAxis,)


class CategoryAxis(QtCharts.QCategoryAxis):
    def __delitem__(self, index: str):
        self.remove(index)

    def __getitem__(self, label: str) -> str:
        return self.categoriesLabels()[label]

    def __setitem__(self, index: str, value: str):
        self.replaceLabel(index, value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.categoriesLabels())

    def __add__(self, other: Tuple[str, int]) -> CategoryAxis:
        self.append(*other)
        return self

    def set_labels_position(self, position: str):
        """Set the labels position.

        Allowed values are "center", "on_value"

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

        Possible values: "center", "on_value"

        Returns:
            labels position
        """
        return LABELS_POSITIONS.inverse[self.labelsPosition()]


if __name__ == "__main__":
    axis = CategoryAxis()
