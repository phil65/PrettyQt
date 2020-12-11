from __future__ import annotations

from typing import Iterator

from qtpy import QtCore


class ItemSelectionRange(QtCore.QItemSelectionRange):
    def __contains__(self, other: QtCore.QModelIndex):
        return self.contains(other)

    def __bool__(self):
        return not self.isEmpty()

    def __iter__(self) -> Iterator[QtCore.QModelIndex]:
        return iter(self.indexes())

    def __len__(self):
        return len(self.indexes())

    def __and__(self, other: QtCore.QItemSelectionRange):
        return self.intersected(other)


if __name__ == "__main__":
    temp = ItemSelectionRange()
    temp2 = ItemSelectionRange()
    temp3 = temp & temp2
