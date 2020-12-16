from typing import List, Optional

from qtpy import QtLocation

from prettyqt import core, location, positioning
from prettyqt.utils import InvalidParamError


class Place(QtLocation.QPlace):
    def __bool__(self):
        return not self.isEmpty()

    def __setitem__(self, index: str, val: Optional[QtLocation.QPlaceAttribute]):
        if val is None:
            val = location.PlaceAttribute()
        self.setExtendedAttribute(index, val)

    def __getitem__(self, index: str) -> location.PlaceAttribute:
        attr = self.extendedAttribute(index)
        return location.PlaceAttribute(attr)

    def get_categories(self) -> List[location.PlaceCategory]:
        return [location.PlaceCategory(i) for i in self.categories()]

    def get_contact_details(self, contact_type: str) -> List[location.PlaceContactDetail]:
        return [location.PlaceContactDetail(i) for i in self.contactDetails(contact_type)]

    def set_content(self, typ: str, value: str):
        if typ not in location.placecontent.TYPE:
            raise InvalidParamError(typ, location.placecontent.TYPE)
        self.setContent(location.placecontent.TYPE[typ], value)

    def get_content(self, typ: str) -> str:
        if typ not in location.placecontent.TYPE:
            raise InvalidParamError(typ, location.placecontent.TYPE)
        return self.content(location.placecontent.TYPE[typ])

    def get_icon(self) -> location.PlaceIcon:
        return location.PlaceIcon(self.icon())

    def get_location(self) -> positioning.GeoLocation:
        return positioning.GeoLocation(self.location())

    def get_primary_website(self) -> core.Url:
        return core.Url(self.primaryWebsite())

    def get_ratings(self) -> location.PlaceRatings:
        return location.PlaceRatings(self.ratings())

    def get_supplier(self) -> location.PlaceSupplier:
        return location.PlaceSupplier(self.supplier())

    def get_visibility(self) -> location.VisibilityStr:
        """Return visibility.

        Returns:
            Visibility
        """
        return location.VISIBILITY.inverse[self.visibility()]


if __name__ == "__main__":
    place = Place()
    attr = location.PlaceAttribute()
    place["test"] = attr
    assert place["test"] == attr
