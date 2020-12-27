from typing import Union

from prettyqt import core, location
from prettyqt.qt import QtCore, QtLocation


class PlaceSupplier(QtLocation.QPlaceSupplier):
    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def set_url(self, url: Union[str, QtCore.QUrl]):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    supplier = PlaceSupplier()
    print(bool(supplier))
