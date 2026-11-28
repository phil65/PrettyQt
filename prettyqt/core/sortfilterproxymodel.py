import contextlib
import enum
import re
from typing import TYPE_CHECKING, Literal

import sublime_search

from prettyqt import constants, core
from prettyqt.utils import bidict


if TYPE_CHECKING:
    from collections.abc import Iterable

    from prettyqt.utils import datatypes


class FilterMode(enum.IntEnum):
    fixed_string = 1
    fuzzy = 2
    wildcard = 4
    regex = 8
    substring = 16


FilterModeStr = Literal["fixed_string", "fuzzy", "wildcard", "regex", "substring"]


FILTER_MODE: bidict[FilterModeStr, FilterMode] = bidict(
    fixed_string=FilterMode.fixed_string,
    fuzzy=FilterMode.fuzzy,
    wildcard=FilterMode.wildcard,
    regex=FilterMode.regex,
    substring=FilterMode.substring,
)

DirectionStr = Literal["rows", "columns", "both"]

DIRECTION: bidict[DirectionStr, core.QSortFilterProxyModel.Direction] = bidict(
    rows=core.QSortFilterProxyModel.Direction.Rows,
    columns=core.QSortFilterProxyModel.Direction.Columns,
    both=core.QSortFilterProxyModel.Direction.Both,
)


class SortFilterProxyModel(core.AbstractProxyModelMixin, core.QSortFilterProxyModel):
    """Support for sorting and filtering data passed between another model and a view."""

    FilterMode = core.Enum(FilterMode)
    invalidated = core.Signal()
    filter_mode_changed = core.Signal(str)
    ID = "sort_filter"
    ICON = "mdi.table-filter"

    def __init__(self, *args, **kwargs):
        self._filter_mode: FilterModeStr = "wildcard"
        super().__init__(*args, **kwargs)

    #     self._filter_column = 0

    # def setFilterKeyColumn(self, column: int | list[int] | None):
    #     if column is None:
    #         column = -1
    #     self._filter_column = column

    # def filterKeyColumn(self) -> int | list[int] | None:
    #     return self._filter_column

    # def filterAcceptsRow(self, source_row: int, source_index: core.ModelIndex):
    #     column = self.filterKeyColumn()
    #     col_count = self.sourceModel().columnCount()
    #     indexes = [
    #         self.sourceModel().index(source_row, i, source_index) for i in col_count
    #     ]
    #     labels = [self.sourceModel().data(idx) for idx in indexes]

    #     if isinstance(column, int) and source_index.column() == column:
    #         return super().filterAcceptsRow(source_row, source_index)

    def filterAcceptsRow(self, source_row: int, source_index: core.ModelIndex) -> bool:
        if self._filter_mode != "fuzzy":
            return super().filterAcceptsRow(source_row, source_index)
        source_model = self.sourceModel()
        if source_model is None:
            return False
        column = self.filterKeyColumn()
        columns = (
            range(source_model.columnCount(source_index)) if column == -1 else [column]
        )
        pattern = self.filterRegularExpression().pattern()
        case_sensitive = self.is_filter_case_sensitive()
        role = self.filterRole()
        for col in columns:
            idx = source_model.index(source_row, col, source_index)
            data = source_model.data(idx, role)
            if data is None:
                continue
            text = data if isinstance(data, str) else str(data)
            if sublime_search.fuzzy_match_simple(
                pattern, text, case_sensitive=case_sensitive
            ):
                return True
        return False

    def invalidate(self):
        super().invalidate()
        self.invalidated.emit()

    @contextlib.contextmanager
    def change_filter(
        self, direction: DirectionStr | core.QSortFilterProxyModel.Direction = "both"
    ):
        """Context manager wrapping beginFilterChange() / endFilterChange()."""
        self.beginFilterChange()
        try:
            yield
        finally:
            self.endFilterChange(DIRECTION.get_enum_value(direction))

    def invalidate_rows_filter(self):
        """Invalidate row filtering using Qt 6.9+ begin/endFilterChange."""
        self.beginFilterChange()
        self.endFilterChange(self.Direction.Rows)

    def lessThan(self, left, right) -> bool:
        role = super().sortRole()
        left_data = left.data(role)
        right_data = right.data(role)
        if left_data is None and right_data is None:
            return False
        if left_data is None:
            return True
        if right_data is None:
            return False
        return left_data < right_data

    def sort(
        self,
        column: int | None,
        ascending: bool | constants.SortOrder = constants.ASCENDING,
    ):
        if isinstance(ascending, bool):
            ascending = constants.ASCENDING if ascending else constants.DESCENDING
        if column is None:
            column = -1
        super().sort(column, ascending)

    def setFilterRegularExpression(self, pattern: datatypes.PatternType | str):
        if isinstance(pattern, re.Pattern):
            pattern = core.RegularExpression(pattern)
        super().setFilterRegularExpression(pattern)

    def setFilterString(self, search_str: str):
        pat = ".*?".join(map(re.escape, search_str))
        pat = f"(?=({pat}))"
        super().setFilterRegularExpression(pat)

    def setFixedFilterList(self, filter_list: Iterable[str]):
        pat = "|".join(filter_list)
        super().setFilterRegularExpression(pat)

    def set_filter_case_sensitivity(
        self, sensitivity: constants.CaseSensitivityStr | constants.CaseSensitivity
    ):
        """Set the filter case sensitivity.

        Args:
            sensitivity: filter case sensitivity
        """
        value = constants.CASE_SENSITIVITY.get_enum_value(sensitivity)
        super().setFilterCaseSensitivity(value)

    def get_filter_case_sensitivity(self) -> constants.CaseSensitivityStr:
        """Return current filter case sensitivity.

        Returns:
            filter case sensitivity
        """
        return constants.CASE_SENSITIVITY.inverse[super().filterCaseSensitivity()]

    def set_filter_case_sensitive(self, state: bool):
        if state:
            sensitivity = constants.CaseSensitivity.CaseSensitive
        else:
            sensitivity = constants.CaseSensitivity.CaseInsensitive
        super().setFilterCaseSensitivity(sensitivity)

    def is_filter_case_sensitive(self) -> bool:
        return super().filterCaseSensitivity() == constants.CaseSensitivity.CaseSensitive

    def set_sort_case_sensitive(self, state: bool):
        if state:
            sensitivity = constants.CaseSensitivity.CaseSensitive
        else:
            sensitivity = constants.CaseSensitivity.CaseInsensitive
        super().setSortCaseSensitivity(sensitivity)

    def is_sort_case_sensitive(self) -> bool:
        return super().sortCaseSensitivity() == constants.CaseSensitivity.CaseSensitive

    def get_filter_regular_expression(self) -> core.RegularExpression:
        return core.RegularExpression(self.filterRegularExpression())

    def set_sort_role(self, role: constants.ItemDataRoleStr | int):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        super().setSortRole(role)

    def set_filter_role(self, role: constants.ItemDataRoleStr | int):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        super().setFilterRole(role)

    def get_sort_order(self) -> Literal["ascending", "descending"]:
        return "ascending" if super().sortOrder() == constants.ASCENDING else "descending"

    def set_filter_key_column(self, column: int | None):
        if column is None:
            column = -1
        super().setFilterKeyColumn(column)

    def set_search_term(self, search_term: str | Iterable[str]):
        if not isinstance(search_term, str):
            if self._filter_mode != "fixed_string":
                raise TypeError(search_term)
            self.setFixedFilterList(list(search_term))
            return
        match self._filter_mode:
            case "fixed_string":
                self.setFilterFixedString(search_term)
            case "substring":
                self.setFilterString(search_term)
            case "fuzzy":
                self.setFilterFixedString(search_term)
            case "wildcard":
                self.setFilterWildcard(search_term)
            case "regex":
                self.setFilterRegularExpression(search_term)

    def get_filter_mode(self) -> FilterModeStr:
        return self._filter_mode

    def set_filter_mode(self, mode: FilterModeStr):
        self._filter_mode = mode
        self.filter_mode_changed.emit(mode)

    filterMode = core.Property(  # noqa: N815
        str,
        get_filter_mode,
        set_filter_mode,
        notify=filter_mode_changed,
        doc="Mode to use for filtering",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    from prettyqt.itemmodels.importlibdistributionmodel import (
        ImportlibTreeModel,
    )

    source_model = ImportlibTreeModel.from_package("prettyqt")
    model = SortFilterProxyModel()
    model.setSourceModel(source_model)
    model.set_filter_mode("fuzzy")
    lineedit = widgets.LineEdit()
    lineedit.value_changed.connect(model.set_search_term)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    widget.box.add(lineedit)
    table = widgets.TableView()
    table.setSortingEnabled(True)
    widget.box.add(table)
    table.set_model(model)
    widget.show()
    app.exec()
