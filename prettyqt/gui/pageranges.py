from __future__ import annotations

from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class PageRanges(QtGui.QPageRanges):
    """Represents a collection of page ranges."""

    def __bool__(self):
        return not self.isEmpty()

    def __getitem__(self, index: int):
        return self.get_range_list()[index]

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return get_repr(self, self.get_range_list())

    def __contains__(self, other: int):
        return self.contains(other)

    def __add__(self, other: int | tuple[int, int]):
        if isinstance(other, int):
            self.addPage(other)
        else:
            self.addRange(*other)
        return self

    def __len__(self):
        return self.lastPage() - self.firstPage()

    def get_range_list(self) -> list[tuple[int, int]]:
        return [(i.from_, i.to) for i in self.toRangeList()]


if __name__ == "__main__":
    ranges = PageRanges()
    ranges.addPage(1)
    ranges.addPage(2)
