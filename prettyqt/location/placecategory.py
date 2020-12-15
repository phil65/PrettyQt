from qtpy import QtLocation

from prettyqt import location


class PlaceCategory(QtLocation.QPlaceCategory):
    def __str__(self):
        return self.name()

    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def get_visibility(self) -> location.VisibilityStr:
        """Return the visibility of the place.

        Returns:
            Visibility
        """
        return location.VISIBILITY.inverse[self.visibility()]


if __name__ == "__main__":
    segment = PlaceCategory()
    print(bool(segment))
