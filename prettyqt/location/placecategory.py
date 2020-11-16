# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import bidict

VISIBILITY = bidict(
    unspecified=QtLocation.QLocation.UnspecifiedVisibility,
    device=QtLocation.QLocation.DeviceVisibility,
    private=QtLocation.QLocation.PrivateVisibility,
    public=QtLocation.QLocation.PublicVisibility,
)


class PlaceCategory(QtLocation.QPlaceCategory):
    def __str__(self):
        return self.name()

    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def get_visibility(self) -> str:
        """Return the visibility of the place.

        Possible values are "unspecified", "device", "private", "public"

        Returns:
            Visibility
        """
        return VISIBILITY.inv[self.visibility()]


if __name__ == "__main__":
    segment = PlaceCategory()
    print(bool(segment))
