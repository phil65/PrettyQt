from __future__ import annotations

from typing import Literal, Optional

from prettyqt import constants, core
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


COMPLETION_MODE = bidict(
    popup=QtWidgets.QCompleter.PopupCompletion,
    inline=QtWidgets.QCompleter.InlineCompletion,
    unfiltered_popup=QtWidgets.QCompleter.UnfilteredPopupCompletion,
)

CompletionModeStr = Literal["popup", "inline", "unfiltered_popup"]

SORT_MODE = bidict(
    unsorted=QtWidgets.QCompleter.UnsortedModel,
    case_sensitive=QtWidgets.QCompleter.CaseSensitivelySortedModel,
    case_insensitive=QtWidgets.QCompleter.CaseInsensitivelySortedModel,
)

SortModeStr = Literal["unsorted", "case_sensitive", "case_insensitive"]


QtWidgets.QCompleter.__bases__ = (core.Object,)


class Completer(QtWidgets.QCompleter):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

    def set_sort_mode(self, mode: Optional[SortModeStr]):
        """Set sort mode to use.

        Args:
            mode: sort mode to use

        Raises:
            InvalidParamError: sort mode does not exist
        """
        if mode is None:
            mode = "unsorted"
        if mode not in SORT_MODE:
            raise InvalidParamError(mode, SORT_MODE)
        self.setModelSorting(SORT_MODE[mode])

    def get_sort_mode(self) -> SortModeStr:
        """Return current sort mode.

        Returns:
            sort mode
        """
        return SORT_MODE.inverse[self.modelSorting()]

    def set_completion_mode(self, mode: CompletionModeStr):
        """Set completion mode to use.

        Args:
            mode: completion mode to use

        Raises:
            InvalidParamError: completion mode does not exist
        """
        if mode not in COMPLETION_MODE:
            raise InvalidParamError(mode, COMPLETION_MODE)
        self.setCompletionMode(COMPLETION_MODE[mode])

    def get_completion_mode(self) -> CompletionModeStr:
        """Return current completion mode.

        Returns:
            completion mode
        """
        return COMPLETION_MODE.inverse[self.completionMode()]

    def set_filter_mode(self, mode: constants.FilterModeStr):
        """Set filter mode to use.

        Args:
            mode: filter mode to use

        Raises:
            InvalidParamError: filter mode does not exist
        """
        if mode not in constants.FILTER_MODES:
            raise InvalidParamError(mode, constants.FILTER_MODES)
        self.setFilterMode(constants.FILTER_MODES[mode])

    def get_filter_mode(self) -> constants.FilterModeStr:
        """Return current filter mode.

        Returns:
            filter mode
        """
        return constants.FILTER_MODES.inverse[self.filterMode()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    completer = Completer()
    app.main_loop()
