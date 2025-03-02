from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core


if TYPE_CHECKING:
    from collections.abc import Iterator


class ItemSelectionRange(core.QItemSelectionRange):
    """Manages information about a range of selected items in a model."""

    def __contains__(self, other: core.ModelIndex):
        return self.contains(other)

    def __bool__(self):
        return not self.isEmpty()

    def __iter__(self) -> Iterator[core.ModelIndex]:
        return iter(self.indexes())  # type: ignore

    def __len__(self):
        return len(self.indexes())

    def __and__(self, other: core.QItemSelectionRange):
        return self.intersected(other)


if __name__ == "__main__":
    temp = ItemSelectionRange()
    temp2 = ItemSelectionRange()
    temp3 = temp & temp2
