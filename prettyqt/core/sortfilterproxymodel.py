from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore


QtCore.QSortFilterProxyModel.__bases__ = (core.AbstractProxyModel,)


class SortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def serialize_fields(self):
        return dict(
            dynamic_sort_filter=self.dynamicSortFilter(),
            is_filter_case_sensitive=self.is_filter_case_sensitive(),
            filter_key_column=self.filterKeyColumn(),
            filter_regular_expression=self.get_filter_regular_expression(),
            filter_role=self.filterRole(),
            is_sort_locale_aware=self.isSortLocaleAware(),
            recursive_filtering_enabled=self.isRecursiveFilteringEnabled(),
            is_sort_case_sensitive=self.is_sort_case_sensitive(),
            sort_role=self.sortRole(),
        )

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

    def set_sort_role(self, role: constants.ItemDataRoleStr):
        self.setSortRole(constants.ITEM_DATA_ROLE[role])
