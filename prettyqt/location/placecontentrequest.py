from __future__ import annotations

from prettyqt import location


class PlaceContentRequest(location.QPlaceContentRequest):
    def set_content_type(
        self, typ: location.placecontent.TypeStr | location.PlaceContent.Type
    ):
        """Set the content type.

        Args:
            typ: Relevance type
        """
        self.setContentType(location.placecontent.TYPE.get_enum_value(typ))

    def get_content_type(self) -> location.placecontent.TypeStr:
        """Return current content type.

        Returns:
            Relevance type
        """
        return location.placecontent.TYPE.inverse[self.contentType()]


if __name__ == "__main__":
    request = PlaceContentRequest()
