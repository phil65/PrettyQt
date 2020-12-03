# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core


class Collator(QtCore.QCollator):
    def get_locale(self) -> core.Locale:
        return core.Locale(self.locale())

    def set_case_sensitive(self, state: bool):
        """Set case sensitivity.

        Args:
            state: case sensitive

        """
        sensitivity = QtCore.Qt.CaseSensitive if state else QtCore.Qt.CaseInsensitive
        self.setCaseSensitivity(sensitivity)

    def is_case_sensitive(self) -> bool:
        """Return case sensitivity.

        Returns:
            case sensitivity
        """
        return bool(self.caseSensitivity())

    def get_sort_key(self, string: str) -> core.CollatorSortKey:
        return core.CollatorSortKey(self.sortKey(string))
