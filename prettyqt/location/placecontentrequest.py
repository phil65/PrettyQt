from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import InvalidParamError


class PlaceContentRequest(QtLocation.QPlaceContentRequest):
    def set_content_type(self, typ: location.placecontent.TypeStr):
        """Set the content type.

        Args:
            typ: Relevance type

        Raises:
            InvalidParamError: content type does not exist
        """
        if typ not in location.placecontent.TYPE:
            raise InvalidParamError(typ, location.placecontent.TYPE)
        self.setContentType(location.placecontent.TYPE[typ])

    def get_content_type(self) -> location.placecontent.TypeStr:
        """Return current content type.

        Returns:
            Relevance type
        """
        return location.placecontent.TYPE.inverse[self.contentType()]


if __name__ == "__main__":
    request = PlaceContentRequest()
    print(bool(request))
