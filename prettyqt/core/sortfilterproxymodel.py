from __future__ import annotations

import re
from typing import Literal

from prettyqt import constants, core
from prettyqt.qt import QtCore


class SortFilterProxyModel(core.AbstractProxyModelMixin, QtCore.QSortFilterProxyModel):
    # def set_filter_case_sensitivity(self, sensitivity: constants.CaseSensitivityStr):
    #     """Set the filter case sensitivity.

    #     Args:
    #         sensitivity: filter case sensitivity

    #     Raises:
    #         InvalidParamError: filter case sensitivity does not exist
    #     """
    #     if sensitivity not in constants.CASE_SENSITIVITY:
    #         raise InvalidParamError(sensitivity, constants.CASE_SENSITIVITY)
    #     self.setFilterCaseSensitivity(constants.CASE_SENSITIVITY[sensitivity])

    # def get_filter_case_sensitivity(self) -> constants.CaseSensitivityStr:
    #     """Return current filter case sensitivity.

    #     Returns:
    #         filter case sensitivity
    #     """
    #     return constants.CASE_SENSITIVITY.inverse[self.filterCaseSensitivity()]

    def setFilterString(self, search_str):
        pat = ".*?".join(map(re.escape, search_str))
        pat = f"(?=({pat}))"
        self.setFilterRegularExpression(pat)

    def set_filter_case_sensitive(self, state: bool):
        if state:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseSensitive
        else:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseInsensitive
        self.setFilterCaseSensitivity(sensitivity)

    def is_filter_case_sensitive(self) -> bool:
        return self.filterCaseSensitivity() == QtCore.Qt.CaseSensitivity.CaseSensitive

    def set_sort_case_sensitive(self, state: bool):
        if state:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseSensitive
        else:
            sensitivity = QtCore.Qt.CaseSensitivity.CaseInsensitive
        self.setSortCaseSensitivity(sensitivity)

    def is_sort_case_sensitive(self) -> bool:
        return self.sortCaseSensitivity() == QtCore.Qt.CaseSensitivity.CaseSensitive

    def get_filter_regular_expression(self) -> core.RegularExpression:
        return core.RegularExpression(self.filterRegularExpression())

    def set_sort_role(self, role: constants.ItemDataRoleStr | int):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        self.setSortRole(role)

    def set_filter_role(self, role: constants.ItemDataRoleStr | int):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        self.setFilterRole(role)

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

    def get_sort_order(self) -> Literal["ascending", "descending"]:
        return "ascending" if self.sortOrder() == constants.ASCENDING else "descending"

    def set_filter_key_column(self, column: int | None):
        if column is None:
            column = -1
        self.setFilterKeyColumn(column)


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
    model = SortFilterProxyModel()
    model.setFilterKeyColumn(1)
    model.setFilterString("ab")
    model.setSourceModel(source_model)
    table = widgets.TreeView()
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
