from __future__ import annotations

from collections.abc import Callable
import dataclasses
import logging
from typing import Any

import sublime_search

from prettyqt import constants, core


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Filter:
    column: int
    value: Any
    role: constants.ItemDataRole


class MultiColumnFilterProxyModel(core.SortFilterProxyModel):
    """A SortFilterProxyModel which filters based on multiple columns in one go.

    This proxy uses seperate search term / values for each column in order to filter
    the source model, thus avoiding to layer proxy models in case you want to filter
    based on several columns. That way it is less demanding since filtering
    for all columns is done in one go.

    This model is used by the [FilterHeader](filterheader.md) widget in order to filter
    a table in one go, avoiding the need to layer multiple proxy models.


    ### Example

    ```py
    proxy = itemmodels.MultiColumnFilterProxyModel()
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "multi_column_filter"

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._filters: dict[int, Filter] = {}
        self.setRecursiveFilteringEnabled(True)

    def clear_filters(self):
        self._filters = {}
        self.invalidateRowsFilter()

    def set_filter_value(
        self,
        column: int,
        value: str,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if value == "" or value is None:  # False is a valid value.
            del self._filters[column]
        else:
            self._filters[column] = Filter(column=column, value=value, role=role)
        self.invalidateRowsFilter()

    def setFilterKeyColumn(self, column: int):
        msg = "Not supported."
        raise NotImplementedError(msg)

    def setFilterRole(self, column: int):
        msg = "Not supported."
        raise NotImplementedError(msg)

    def filterAcceptsRow(self, row, parent):
        source = self.sourceModel()
        for k, v in self._filters.items():
            index = source.index(row, k, parent)
            data = source.data(index, v.role)
            search_val = v.value
            match search_val:
                case str():
                    search_val = str(search_val)
                    data = str(data)
                    if (
                        self.filterMode == "fuzzy"
                        and not sublime_search.fuzzy_match_simple(
                            search_val,
                            data,
                            case_sensitive=self.is_filter_case_sensitive(),
                        )
                    ):
                        return False
                    if not self.is_filter_case_sensitive():
                        search_val = search_val.lower()
                        data = data.lower()
                    if not data.startswith(search_val):
                        return False
                case Callable():
                    return search_val(data)
                case _:
                    if data != search_val:
                        return False
        return True


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_tree()
    model = MultiColumnFilterProxyModel()
    model.setSourceModel(table.model())
    table.setRootIsDecorated(True)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
