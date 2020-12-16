from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import bidict


TYPE = bidict(
    none=QtLocation.QPlaceContent.NoType,
    image=QtLocation.QPlaceContent.ImageType,
    review=QtLocation.QPlaceContent.ReviewType,
    editorial=QtLocation.QPlaceContent.EditorialType,
    custom=QtLocation.QPlaceContent.CustomType,
)


class PlaceContent(QtLocation.QPlaceContent):
    def get_type(self) -> str:
        """Return the visibility of the place.

        Possible values are "none", "image", "review", "editorial", "custom"

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
