from __future__ import annotations

from prettyqt.qt import QtWidgets


class TableWidgetSelectionRange(QtWidgets.QTableWidgetSelectionRange):
    def __repr__(self):
        return (
            f"{type(self).__name__}({self.topRow()}, {self.leftColumn()}, "
            f"{self.bottomRow()}, {self.rightColumn()})"
        )

    def __eq__(self, other: object):
        if not isinstance(other, TableWidgetSelectionRange):
            return False
        return (
            self.topRow() == other.topRow()
            and self.bottomRow() == other.bottomRow()
            and self.leftColumn() == other.leftColumn()
            and self.rightColumn() == other.rightColumn()
        )

    def __or__(
        self, other: QtWidgets.QTableWidgetSelectionRange
    ) -> TableWidgetSelectionRange:
        return TableWidgetSelectionRange(
            min(self.topRow(), other.topRow()),
            min(self.leftColumn(), other.leftColumn()),
            max(self.bottomRow(), other.bottomRow()),
            max(self.rightColumn(), other.rightColumn()),
        )

    def __and__(
        self, other: QtWidgets.QTableWidgetSelectionRange
    ) -> TableWidgetSelectionRange:
        if not (
            other.topRow() <= self.bottomRow()
            or other.bottomRow() >= self.topRow()
            or other.leftColumn() <= self.rightColumn()
            or other.rightColumn() >= self.leftColumn()
        ):
            return TableWidgetSelectionRange()
        return TableWidgetSelectionRange(
            max(self.topRow(), other.topRow()),
            max(self.leftColumn(), other.leftColumn()),
            min(self.bottomRow(), other.bottomRow()),
            min(self.rightColumn(), other.rightColumn()),
        )


if __name__ == "__main__":
    range_1 = TableWidgetSelectionRange(0, 0, 10, 10)
    range_2 = TableWidgetSelectionRange(5, 5, 15, 15)
    result = range_1 == range_2
    print(result)
