from __future__ import annotations

from prettyqt import core
from prettyqt.utils import get_repr


class ValueFilterProxyModel(core.SortFilterProxyModel):
    """Proxy model for filtering based on non-str values.

    Sometimes it is needed to filter for non-str values, especially when it is required
    to filter based on a different role than DisplayRole.

    Same as the Qt QSortFilterProxyModel, this proxy respects the filterRole and
    filterKeyColumn properties.
    """

    ID = "value_filter"

    def __init__(self, filter_value=None, **kwargs):
        self._filter_value = filter_value
        super().__init__(**kwargs)

    def __repr__(self):
        return get_repr(self, self._filter_value)

    def filterAcceptsRow(self, source_row: int, parent: core.ModelIndex) -> bool:
        if self._filter_value is None:
            return True
        column = self.filterKeyColumn()
        role = self.filterRole()
        source_model = self.sourceModel()
        idx = source_model.index(source_row, column, parent)
        value = source_model.data(idx, role)
        return value == self._filter_value

    def set_filter_value(self, value):
        """Set the filter value."""
        self._filter_value = value
        self.invalidateRowsFilter()

    def get_filter_value(self):
        """Get the filter value."""
        return self._filter_value

    filter_value = core.Property(object, get_filter_value, set_filter_value, user=True)


if __name__ == "__main__":
    from prettyqt import constants, widgets

    app = widgets.app()
    proxy = ValueFilterProxyModel(True, filter_role=constants.CHECKSTATE_ROLE)
