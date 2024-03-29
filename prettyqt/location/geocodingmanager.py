from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtLocation


class GeoCodingManager(core.ObjectMixin):
    """Support for geocoding operations."""

    def __init__(self, item: QtLocation.QGeoCodingManager):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    def get_locale(self) -> core.Locale:
        return core.Locale(self.item.locale())
