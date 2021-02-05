from __future__ import annotations

from prettyqt import core, location
from prettyqt.qt import QtCore, QtLocation


QtLocation.QPlaceImage.__bases__ = (location.PlaceContent,)


class PlaceImage(QtLocation.QPlaceImage):
    def __str__(self):
        return self.imageId()

    def set_url(self, url: str | QtCore.QUrl):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    image = PlaceImage()
