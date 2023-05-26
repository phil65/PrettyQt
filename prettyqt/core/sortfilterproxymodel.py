from __future__ import annotations

from collections.abc import Iterable
import re
from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


class SortFilterProxyModel(core.AbstractProxyModelMixin, QtCore.QSortFilterProxyModel):
    invalidated = core.Signal()
    ID = "sort_filter"
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
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

    def invalidate(self):
        super().invalidate()
        self.invalidated.emit()

    def lessThan(self, left, right):
        role = super().sortRole()
        left_data = left.data(role)
        right_data = right.data(role)
        if left_data is not None and right_data is not None:
            return left_data < right_data
        return True

    def sort(
        self,
        column: int | None,
        ascending: bool | QtCore.Qt.SortOrder = constants.ASCENDING,
    ):
        if isinstance(ascending, bool):
            ascending = constants.ASCENDING if ascending else constants.DESCENDING
        if column is None:
            column = -1
        super().sort(column, ascending)

    def setFilterString(self, search_str: str):
        pat = ".*?".join(map(re.escape, search_str))
        pat = f"(?=({pat}))"
        super().setFilterRegularExpression(pat)

    def setFixedFilterList(self, filter_list: Iterable[str]):
        pat = "|".join(filter_list)
        super().setFilterRegularExpression(pat)

    def set_filter_case_sensitivity(self, sensitivity: constants.CaseSensitivityStr):
        """Set the filter case sensitivity.

        Args:
            sensitivity: filter case sensitivity

        Raises:
            InvalidParamError: filter case sensitivity does not exist
        """
        if sensitivity not in constants.CASE_SENSITIVITY:
            raise InvalidParamError(sensitivity, constants.CASE_SENSITIVITY)
        super().setFilterCaseSensitivity(constants.CASE_SENSITIVITY[sensitivity])

    def get_filter_case_sensitivity(self) -> constants.CaseSensitivityStr:
        """Return current filter case sensitivity.

        Returns:
            filter case sensitivity
        """
        return constants.CASE_SENSITIVITY.inverse[super().filterCaseSensitivity()]

    def set_filter_case_sensitive(self, state: bool):
        if state:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseSensitive
        else:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseInsensitive
        super().setFilterCaseSensitivity(sensitivity)

    def is_filter_case_sensitive(self) -> bool:
        return super().filterCaseSensitivity() == QtCore.Qt.CaseSensitivity.CaseSensitive

    def set_sort_case_sensitive(self, state: bool):
        if state:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseSensitive
        else:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseInsensitive
        super().setSortCaseSensitivity(sensitivity)

    def is_sort_case_sensitive(self) -> bool:
        return super().sortCaseSensitivity() == QtCore.Qt.CaseSensitivity.CaseSensitive

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


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "axxxb",
            },
        ),
        6,
        "jkjk",
    ]
    source_model = JsonModel(dist)
    from prettyqt.custom_models.importlibdistributionmodel import (
        ImportlibDistributionModel,
    )

    source_model = ImportlibDistributionModel.from_package("prettyqt")
    model = SortFilterProxyModel()
    model.setSourceModel(source_model)
    lineedit = widgets.LineEdit()
    # completer = SubsequenceCompleter()
    # completer.setModel(source_model)
    # lineedit.set_completer(completer)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    widget.box.add(lineedit)
    table = widgets.TableView()
    table.setSortingEnabled(True)
    widget.box.add(table)
    table.set_model(model)
    widget.show()
    app.main_loop()
