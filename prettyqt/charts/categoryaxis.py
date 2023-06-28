from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from prettyqt import charts
from prettyqt.utils import bidict


LABELS_POSITIONS = bidict(
    center=charts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionCenter,
    on_value=charts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue,
)

LabelsPositionStr = Literal["center", "on_value"]


class CategoryAxis(charts.ValueAxisMixin, charts.QCategoryAxis):
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
        # needed for PySide6
        return self.count()

    def set_labels_position(
        self, position: LabelsPositionStr | charts.QCategoryAxis.AxisLabelsPosition
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


if __name__ == "__main__":
    axis = CategoryAxis()
