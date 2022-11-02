from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import charts
from prettyqt.qt import QtCharts
from prettyqt.utils import InvalidParamError, bidict


LABELS_POSITIONS = bidict(
    center=QtCharts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionCenter,
    on_value=QtCharts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue,
)

LabelsPositionStr = Literal["center", "on_value"]

QtCharts.QCategoryAxis.__bases__ = (charts.ValueAxis,)


class CategoryAxis(QtCharts.QCategoryAxis):
    def __delitem__(self, index: str):
        self.remove(index)

    def __getitem__(self, label: int | slice) -> str | list[str]:
        return self.categoriesLabels()[label]

    def __setitem__(self, index: str, value: str):
        self.replaceLabel(index, value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.categoriesLabels())

    def __add__(self, other: tuple[str, int]) -> CategoryAxis:
        self.append(*other)
        return self

    def __len__(self):
        # needed for PySide2
        return self.count()

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


if __name__ == "__main__":
    axis = CategoryAxis()
