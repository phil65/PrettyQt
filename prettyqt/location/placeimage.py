from typing import Union

from qtpy import QtCore, QtLocation

from prettyqt import core, location


QtLocation.QPlaceImage.__bases__ = (location.PlaceContent,)


class PlaceImage(QtLocation.QPlaceImage):
    def __str__(self):
        return self.imageId()

    def set_url(self, url: Union[str, QtCore.QUrl]):
        url = core.Url(url)
        self.setUrl(url)

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    image = PlaceImage()
