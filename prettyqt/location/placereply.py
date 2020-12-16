from qtpy import QtLocation

from prettyqt import core
from prettyqt.utils import bidict


ERROR = bidict(
    none=QtLocation.QPlaceReply.NoError,
    place_does_not_exist=QtLocation.QPlaceReply.PlaceDoesNotExistError,
    category_does_not_exist=QtLocation.QPlaceReply.CategoryDoesNotExistError,
    communication=QtLocation.QPlaceReply.CommunicationError,
    parse=QtLocation.QPlaceReply.ParseError,
    permissions=QtLocation.QPlaceReply.PermissionsError,
    unsupported=QtLocation.QPlaceReply.UnsupportedError,
    bad_argument=QtLocation.QPlaceReply.BadArgumentError,
    cancel=QtLocation.QPlaceReply.CancelError,
    unknown=QtLocation.QPlaceReply.UnknownError,
)

TYPE = bidict(
    generic=QtLocation.QPlaceReply.Reply,
    details=QtLocation.QPlaceReply.DetailsReply,
    search=QtLocation.QPlaceReply.SearchReply,
    search_suggestion=QtLocation.QPlaceReply.SearchSuggestionReply,
    content=QtLocation.QPlaceReply.ContentReply,
    id=QtLocation.QPlaceReply.IdReply,
    match=QtLocation.QPlaceReply.MatchReply,
)

QtLocation.QPlaceReply.__bases__ = (core.Object,)


class PlaceReply(QtLocation.QPlaceReply):
    def get_error(self) -> str:
        """Return error type.

        possible values: "none" "place_does_not_exist", "category_does_not_exist",
                         "communication", "parse", "permissions", "unsupported",
                         "bad_argument", "cancel", "unknown"

        Returns:
            Error type
        """
        return ERROR.inverse[self.error()]

    def get_type(self) -> str:
        """Return type.

        possible values: "generic" "details", "search",
                         "search_suggestion", "content", "id", "match",

        Returns:
            Type
        """
        return TYPE.inverse[self.type()]


if __name__ == "__main__":
    reply = PlaceReply()
