from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict


CompletionModeStr = Literal["popup", "inline", "unfiltered_popup"]

COMPLETION_MODE: bidict[CompletionModeStr, widgets.QCompleter.CompletionMode] = bidict(
    popup=widgets.QCompleter.CompletionMode.PopupCompletion,
    inline=widgets.QCompleter.CompletionMode.InlineCompletion,
    unfiltered_popup=widgets.QCompleter.CompletionMode.UnfilteredPopupCompletion,
)


SortModeStr = Literal["unsorted", "case_sensitive", "case_insensitive"]

SORT_MODE: bidict[SortModeStr, widgets.QCompleter.ModelSorting] = bidict(
    unsorted=widgets.QCompleter.ModelSorting.UnsortedModel,
    case_sensitive=widgets.QCompleter.ModelSorting.CaseSensitivelySortedModel,
    case_insensitive=widgets.QCompleter.ModelSorting.CaseInsensitivelySortedModel,
)


class Completer(core.ObjectMixin, widgets.QCompleter):
    """Completions based on an item model."""

    path_updated = core.Signal(str)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "caseSensitivity": constants.CASE_SENSITIVITY,
            "completionMode": COMPLETION_MODE,
            "modelSorting": SORT_MODE,
            "filterMode": constants.MATCH_FLAGS,
        }
        return maps

    def splitPath(self, path: str) -> list[str]:
        self.path_updated.emit(path)
        return super().splitPath(path)

    def get_completions(self) -> list[str]:
        completions = []
        # count = self.completionCount()
        # for i in range(count):
        #     self.setCurrentRow(i)
        #     completions.append(self.currentCompletion())
        # according to docs, completionCount should be avoided. Not sure if thats true.
        i = 0
        while self.setCurrentRow(i):
            completions.append(self.currentCompletion())
            i += 1
        return completions

    def set_strings(self, strings: list[str]):
        model = core.StringListModel(strings)
        self.setModel(model)

    def set_sort_mode(self, mode: SortModeStr | widgets.QCompleter.ModelSorting | None):
        """Set sort mode to use.

        Args:
            mode: sort mode to use
        """
        if mode is None:
            mode = "unsorted"
        self.setModelSorting(SORT_MODE.get_enum_value(mode))

    def get_sort_mode(self) -> SortModeStr:
        """Return current sort mode.

        Returns:
            sort mode
        """
        return SORT_MODE.inverse[self.modelSorting()]

    def set_completion_mode(
        self, mode: CompletionModeStr | widgets.QCompleter.CompletionMode
    ):
        """Set completion mode to use.

        Args:
            mode: completion mode to use
        """
        self.setCompletionMode(COMPLETION_MODE.get_enum_value(mode))

    def get_completion_mode(self) -> CompletionModeStr:
        """Return current completion mode.

        Returns:
            completion mode
        """
        return COMPLETION_MODE.inverse[self.completionMode()]

    def set_filter_mode(self, mode: constants.FilterModeStr | constants.MatchFlag):
        """Set filter mode to use.

        Args:
            mode: filter mode to use
        """
        self.setFilterMode(constants.FILTER_MODES.get_enum_value(mode))

    def get_filter_mode(self) -> constants.FilterModeStr:
        """Return current filter mode.

        Returns:
            filter mode
        """
        return constants.FILTER_MODES.inverse[self.filterMode()]

    def set_case_sensitive(self, state: bool):
        """Set case sensitivity.

        Args:
            state: case sensitive

        """
        sensitivity = (
            constants.CaseSensitivity.CaseSensitive
            if state
            else constants.CaseSensitivity.CaseInsensitive
        )
        self.setCaseSensitivity(sensitivity)

    def is_case_sensitive(self) -> bool:
        """Return case sensitivity.

        Returns:
            case sensitivity
        """
        return self.caseSensitivity() == constants.CaseSensitivity.CaseSensitive

    def set_completion_role(
        self, role: constants.ItemDataRoleStr | constants.ItemDataRole | int
    ):
        role = constants.ITEM_DATA_ROLE[role] if isinstance(role, str) else role
        self.setCompletionRole(role)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    completer = Completer()
    model = widgets.FileSystemModel()
    model.set_root_path("")
    app.sleep(10)
    completer.setModel(model)
