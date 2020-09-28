# -*- coding: utf-8 -*-

from typing import Optional

from qtpy import QtWidgets, QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


COMPLETION_MODES = bidict(
    popup=QtWidgets.QCompleter.PopupCompletion,
    inline=QtWidgets.QCompleter.InlineCompletion,
    unfiltered_popup=QtWidgets.QCompleter.UnfilteredPopupCompletion,
)

SORT_MODES = bidict(
    unsorted=QtWidgets.QCompleter.UnsortedModel,
    case_sensitive=QtWidgets.QCompleter.CaseSensitivelySortedModel,
    case_insensitive=QtWidgets.QCompleter.CaseInsensitivelySortedModel,
)

FILTER_MODES = bidict(
    starts_with=QtCore.Qt.MatchStartsWith,
    contains=QtCore.Qt.MatchContains,
    ends_with=QtCore.Qt.MatchEndsWith,
)


QtWidgets.QCompleter.__bases__ = (core.Object,)


class Completer(QtWidgets.QCompleter):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

    def set_sort_mode(self, mode: Optional[str]):
        """Set sort mode to use.

        Allowed values are "unsorted", "case_sensitive", "case_insensitive"

        Args:
            mode: sort mode to use

        Raises:
            InvalidParamError: sort mode does not exist
        """
        if mode is None:
            mode = "unsorted"
        if mode not in SORT_MODES:
            raise InvalidParamError(mode, SORT_MODES)
        self.setModelSorting(SORT_MODES[mode])

    def get_sort_mode(self) -> str:
        """Return current sort mode.

        Possible values: "unsorted", "case_sensitive", "case_insensitive"

        Returns:
            sort mode
        """
        return SORT_MODES.inv[self.modelSorting()]

    def set_completion_mode(self, mode: str):
        """Set completion mode to use.

        Allowed values are "popup", "inline", "unfiltered_popup"

        Args:
            mode: completion mode to use

        Raises:
            InvalidParamError: completion mode does not exist
        """
        if mode not in COMPLETION_MODES:
            raise InvalidParamError(mode, COMPLETION_MODES)
        self.setCompletionMode(COMPLETION_MODES[mode])

    def get_completion_mode(self) -> str:
        """Return current completion mode.

        Possible values: "popup", "inline", "unfiltered_popup"

        Returns:
            completion mode
        """
        return COMPLETION_MODES.inv[self.completionMode()]

    def set_filter_mode(self, mode: str):
        """Set filter mode to use.

        Allowed values are "starts_with", "contains", "ends_with"

        Args:
            mode: filter mode to use

        Raises:
            InvalidParamError: filter mode does not exist
        """
        if mode not in FILTER_MODES:
            raise InvalidParamError(mode, FILTER_MODES)
        self.setFilterMode(FILTER_MODES[mode])

    def get_filter_mode(self) -> str:
        """Return current filter mode.

        Possible values: "starts_with", "contains", "ends_with"

        Returns:
            filter mode
        """
        return FILTER_MODES.inv[self.filterMode()]


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    completer = Completer()
    app.main_loop()
