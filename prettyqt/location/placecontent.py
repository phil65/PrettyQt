from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


TYPE = bidict(
    none=QtLocation.QPlaceContent.Type.NoType,
    image=QtLocation.QPlaceContent.Type.ImageType,
    review=QtLocation.QPlaceContent.Type.ReviewType,
    editorial=QtLocation.QPlaceContent.Type.EditorialType,
    custom=QtLocation.QPlaceContent.Type.CustomType,
)

TypeStr = Literal["none", "image", "review", "editorial", "custom"]


class PlaceContentMixin:
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


class PlaceContent(PlaceContentMixin, QtLocation.QPlaceContent):
    pass


if __name__ == "__main__":
    content = PlaceContent()
