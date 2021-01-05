from __future__ import annotations

from typing import Optional, Union

from prettyqt import core, location
from prettyqt.qt import QtCore, QtLocation


class PlaceSupplier(QtLocation.QPlaceSupplier):
    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> Optional[location.PlaceIcon]:
        icon = self.icon()
        if icon.isEmpty():
            return None
        return location.PlaceIcon(icon)

    def set_url(self, url: Union[str, QtCore.QUrl]):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    supplier = PlaceSupplier()
    print(bool(supplier))
