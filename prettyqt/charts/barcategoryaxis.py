from __future__ import annotations

from prettyqt import charts


class BarCategoryAxis(charts.AbstractAxisMixin, charts.QBarCategoryAxis):
    def __delitem__(self, index: str):
        """Remove category."""
        self.remove(index)

    def __getitem__(self, index: int) -> str:
        """Return category for given index."""
        return self.categories()[index]

    def __setitem__(self, index: str, value: str):
        """Set category at given index to value."""
        self.replace(index, value)

    def __add__(self, other: str) -> BarCategoryAxis:
        """Append another category to axis."""
        self.append(other)
        return self
