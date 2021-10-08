from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class Collator(QtCore.QCollator):
    def __repr__(self):
        return f"{type(self).__name__}({self.get_locale()!r})"

    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def set_case_sensitive(self, state: bool):
        """Set case sensitivity.

        Args:
            state: case sensitive

        """
        sensitivity = (
            QtCore.Qt.CaseSensitivity.CaseSensitive
            if state
            else QtCore.Qt.CaseSensitivity.CaseInsensitive
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
