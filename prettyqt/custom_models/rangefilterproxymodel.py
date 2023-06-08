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
        if self._min_value is None:
            return True
        column = self.filterKeyColumn()
        role = self.filterRole()
        source_model = self.sourceModel()
        idx = source_model.index(source_row, column, parent)
        value = source_model.data(idx, role)
        if self._min_value is not None and value < self._min_value:
            return False
        return self._max_value is None or value <= self._max_value

    def set_min_value(self, value):
        self._min_value = value
        self.invalidateRowsFilter()

    def get_min_value(self):
        return self._min_value

    def set_max_value(self, value):
        self._max_value = value
        self.invalidateRowsFilter()

    def get_max_value(self):
        return self._max_value

    def set_range(self, range_: tuple[int, int]):
        self._min_value, self._max_value = range_
        self.invalidateRowsFilter()

    def get_range(self) -> tuple[int, int]:
        return (self._min_value, self._max_value)

    value_range = core.Property(object, get_range, set_range, user=True)


if __name__ == "__main__":
    from prettyqt import constants, widgets

    app = widgets.app()
    proxy = RangeFilterProxyModel(True, filter_role=constants.CHECKSTATE_ROLE)
