from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


TYPE = bidict(
    none=QtLocation.QPlaceContent.NoType,
    image=QtLocation.QPlaceContent.ImageType,
    review=QtLocation.QPlaceContent.ReviewType,
    editorial=QtLocation.QPlaceContent.EditorialType,
    custom=QtLocation.QPlaceContent.CustomType,
)

TypeStr = Literal["none", "image", "review", "editorial", "custom"]


class PlaceContent(QtLocation.QPlaceContent):
    def get_type(self) -> TypeStr:
        """Return the visibility of the place.

        Returns:
            Place type
        """
        return TYPE.inverse[self.type()]

    def get_user(self) -> location.PlaceUser:
        return location.PlaceUser(self.user())

    def get_supplier(self) -> location.PlaceSupplier:
        return location.PlaceSupplier(self.supplier())


if __name__ == "__main__":
    content = PlaceContent()
