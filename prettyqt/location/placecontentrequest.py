from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import InvalidParamError


class PlaceContentRequest(QtLocation.QPlaceContentRequest):
    def set_content_type(self, typ: str):
        """Set the content type.

        Allowed values are "none", "image", "review", "editorial", "custom"

        Args:
            typ: Relevance type

        Raises:
            InvalidParamError: content type does not exist
        """
        if typ not in location.placecontent.TYPE:
            raise InvalidParamError(typ, location.placecontent.TYPE)
        self.setContentType(location.placecontent.TYPE[typ])

    def get_content_type(self) -> str:
        """Return current content type.

        Possible values: "none", "image", "review", "editorial", "custom"

        Returns:
            Relevance type
        """
        return location.placecontent.TYPE.inverse[self.contentType()]


if __name__ == "__main__":
    request = PlaceContentRequest()
    print(bool(request))
