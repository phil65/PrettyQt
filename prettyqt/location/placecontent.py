from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.utils import bidict


TYPE = bidict(
    none=location.QPlaceContent.Type.NoType,
    image=location.QPlaceContent.Type.ImageType,
    review=location.QPlaceContent.Type.ReviewType,
    editorial=location.QPlaceContent.Type.EditorialType,
    custom=location.QPlaceContent.Type.CustomType,
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


class PlaceContent(PlaceContentMixin, location.QPlaceContent):
    """Holds content about places."""


if __name__ == "__main__":
    content = PlaceContent()
