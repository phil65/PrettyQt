from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from prettyqt import charts
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Iterator


LabelsPositionStr = Literal["center", "on_value"]

LABELS_POSITIONS: bidict[LabelsPositionStr, charts.QCategoryAxis.AxisLabelsPosition] = (
    bidict(
        center=charts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionCenter,
        on_value=charts.QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue,
    )
)


class CategoryAxis(charts.ValueAxisMixin, charts.QCategoryAxis):
    def __delitem__(self, index: str):
        """Remove category label."""
        self.remove(index)

    def __getitem__(self, label: int | slice) -> str | list[str]:
        """Get category label from given index."""
        return self.categoriesLabels()[label]

    def __setitem__(self, index: str, value: str):
        """Set label at given index to value."""
        self.replaceLabel(index, value)

    def __iter__(self) -> Iterator[str]:
        """Iterate through all category labels."""
        return iter(self.categoriesLabels())

    def __add__(self, other: tuple[str, int]) -> CategoryAxis:
        """Append another category."""
        self.append(*other)
        return self

    def __len__(self):
        """Return category label count from axis."""
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
