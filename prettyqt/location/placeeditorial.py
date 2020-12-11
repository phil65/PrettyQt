from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceEditorial.__bases__ = (location.PlaceContent,)


class PlaceEditorial(QtLocation.QPlaceEditorial):
    def __str__(self):
        return f"{self.title()}: {self.text()}"


if __name__ == "__main__":
    image = PlaceEditorial()
