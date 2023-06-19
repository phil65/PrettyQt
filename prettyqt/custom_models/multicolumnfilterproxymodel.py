from __future__ import annotations

from typing import Any
import dataclasses
import logging

from prettyqt import constants, core
from prettyqt.utils import fuzzy

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Filter:
    column: int
    value: Any
    role: constants.ItemDataRole


class MultiColumnFilterProxyModel(core.SortFilterProxyModel):
    """A SortFilterProxyModel which filters based on multiple columns in one go.

    Especially useful for our FilterHeader widget, which otherwise would nest
    a lot of SortFilterProxyModels, where each one would have to loop the whole table.
    """

    ID = "multi_column_filter"

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._filters: dict[int, Filter] = {}

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
        raise NotImplementedError("Not supported.")

    def setFilterRole(self, column: int):
        raise NotImplementedError("Not supported.")

    def filterAcceptsRow(self, row, parent):
        source = self.sourceModel()
        for k, v in self._filters.items():
            index = source.index(row, k, parent)
            data = source.data(index, v.role)
            search_val = v.value
            match search_val:
                case str():
                    if (
                        self.filterMode == "fuzzy"
                        and not fuzzy.fuzzy_match_simple(
                            search_val,
                            data,
                            case_sensitive=self.is_filter_case_sensitive(),
                        )
                    ):
                        return False
                    if self.is_filter_case_sensitive():
                        search_val = search_val.lower()
                        data = data.lower()
                    if not search_val.startswith(data):
                        return False
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
        app.main_loop()
