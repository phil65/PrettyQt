from typing import List

from qtpy import QtCore

from prettyqt import core


QtCore.QSortFilterProxyModel.__bases__ = (core.AbstractProxyModel,)


class SortFilterProxyModel(QtCore.QSortFilterProxyModel):

    HEADER: List[str] = []

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
            sensitivity = QtCore.Qt.CaseSensitive
        else:
            sensitivity = QtCore.Qt.CaseInsensitive
        self.setFilterCaseSensitivity(sensitivity)

    def is_filter_case_sensitive(self) -> bool:
        return self.filterCaseSensitivity() == QtCore.Qt.CaseSensitive
