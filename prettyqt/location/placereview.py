from qtpy import QtLocation

from prettyqt import core, location


QtLocation.QPlaceReview.__bases__ = (location.PlaceContent,)


class PlaceReview(QtLocation.QPlaceReview):
    def __str__(self):
        return f"{self.title()}: {self.text()}"

    def get_datetime(self) -> core.DateTime:
        return core.DateTime(self.dateTime())


if __name__ == "__main__":
    image = PlaceReview()
