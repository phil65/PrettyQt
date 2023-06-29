from __future__ import annotations

from prettyqt import core
from prettyqt.utils import get_repr


class RangeFilterProxyModel(core.SortFilterProxyModel):
    ID = "range_filter"

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(**kwargs)

    def __repr__(self):
        return get_repr(self, self.get_range)

    def filterAcceptsRow(self, source_row: int, parent: core.ModelIndex) -> bool:
        column = self.filterKeyColumn()
        role = self.filterRole()
        source_model = self.sourceModel()
        idx = source_model.index(source_row, column, parent)
        value = source_model.data(idx, role)
        if self._min_value is not None and value < self._min_value:
            return False
        return self._max_value is None or value <= self._max_value

    def set_min_value(self, value: float | int | None):
        self._min_value = value
        self.invalidateRowsFilter()

    def get_min_value(self) -> float | int:
        if self._min_value is None:
            return -float("inf")
        return self._min_value

    def set_max_value(self, value: float | int):
        self._max_value = value
        self.invalidateRowsFilter()

    def get_max_value(self) -> float | int:
        if self._max_value is None:
            return float("inf")
        return self._max_value

    def set_range(self, rng: tuple[float | int | None, float | int | None]):
        self._min_value, self._max_value = rng
        self.invalidateRowsFilter()

    def get_range(self) -> tuple[float | int | None, float | int | None]:
        return (self._min_value, self._max_value)

    min_value = core.Property(float, get_min_value, set_min_value)
    max_value = core.Property(float, get_max_value, set_max_value)


if __name__ == "__main__":
    from prettyqt import constants, widgets

    app = widgets.app()
    proxy = RangeFilterProxyModel(True, filter_role=constants.CHECKSTATE_ROLE)
