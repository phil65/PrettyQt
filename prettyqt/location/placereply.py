from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict


ERROR = bidict(
    none=QtLocation.QPlaceReply.Error.NoError,
    place_does_not_exist=QtLocation.QPlaceReply.Error.PlaceDoesNotExistError,
    category_does_not_exist=QtLocation.QPlaceReply.Error.CategoryDoesNotExistError,
    communication=QtLocation.QPlaceReply.Error.CommunicationError,
    parse=QtLocation.QPlaceReply.Error.ParseError,
    permissions=QtLocation.QPlaceReply.Error.PermissionsError,
    unsupported=QtLocation.QPlaceReply.Error.UnsupportedError,
    bad_argument=QtLocation.QPlaceReply.Error.BadArgumentError,
    cancel=QtLocation.QPlaceReply.Error.CancelError,
    unknown=QtLocation.QPlaceReply.Error.UnknownError,
)

ErrorStr = Literal[
    "none",
    "place_does_not_exist",
    "category_does_not_exist",
    "communication",
    "parse",
    "permissions",
    "unsupported",
    "bad_argument",
    "cancel",
    "unknown",
]

TYPE = bidict(
    generic=QtLocation.QPlaceReply.Type.Reply,
    details=QtLocation.QPlaceReply.Type.DetailsReply,
    search=QtLocation.QPlaceReply.Type.SearchReply,
    search_suggestion=QtLocation.QPlaceReply.Type.SearchSuggestionReply,
    content=QtLocation.QPlaceReply.Type.ContentReply,
    id=QtLocation.QPlaceReply.Type.IdReply,
    match=QtLocation.QPlaceReply.Type.MatchReply,
)

TypeStr = Literal[
    "generic",
    "details",
    "search",
    "search_suggestion",
    "content",
    "id",
    "match",
]


class PlaceReplyMixin(core.ObjectMixin):
    def get_error(self) -> ErrorStr:
        """Return error type.

        Returns:
            Error type
        """
        return ERROR.inverse[self.error()]

    def get_type(self) -> TypeStr:
        """Return type.

        Returns:
            Type
        """
        return TYPE.inverse[self.type()]


class PlaceReply(PlaceReplyMixin, QtLocation.QPlaceReply):
    pass


if __name__ == "__main__":
    reply = PlaceReply()
