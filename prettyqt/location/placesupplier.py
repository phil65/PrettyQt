from __future__ import annotations

from prettyqt import core, location
from prettyqt.qt import QtLocation
from prettyqt.utils import types


class PlaceSupplier(QtLocation.QPlaceSupplier):
    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> location.PlaceIcon | None:
        icon = self.icon()
        if icon.isEmpty():
            return None
        return location.PlaceIcon(icon)

    def set_url(self, url: types.UrlType):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    supplier = PlaceSupplier()
    print(bool(supplier))
