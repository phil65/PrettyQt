from typing import TYPE_CHECKING, Literal

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


if TYPE_CHECKING:
    from prettyqt.qt import QtLocation

    _PlaceContentBase = QtLocation.QPlaceContent
else:
    _PlaceContentBase = object


class PlaceContentMixin(_PlaceContentBase):
    def get_type(self) -> TypeStr:
        """Return the content type.

        Returns:
            Content type
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
