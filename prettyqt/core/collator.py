from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class Collator(QtCore.QCollator):
    def __repr__(self):
        return get_repr(self, self.get_locale())

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

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
        return bool(self.caseSensitivity())

    def get_sort_key(self, string: str) -> core.CollatorSortKey:
        return core.CollatorSortKey(self.sortKey(string))
