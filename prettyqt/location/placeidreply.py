from __future__ import annotations

from typing import Literal

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import bidict, get_repr


OPERATION_TYPES = bidict(
    save_place=QtLocation.QPlaceIdReply.OperationType.SavePlace,
    remove_place=QtLocation.QPlaceIdReply.OperationType.RemovePlace,
    save_category=QtLocation.QPlaceIdReply.OperationType.SaveCategory,
    remove_category=QtLocation.QPlaceIdReply.OperationType.RemoveCategory,
)

OperationTypeStr = Literal[
    "save_place", "remove_place", "save_category", "remove_category"
]


class PlaceIdReply(location.PlaceReplyMixin, QtLocation.QPlaceIdReply):
    def __repr__(self):
        return get_repr(self, self.operationType())

    @classmethod
    def clone_from(cls, obj: QtLocation.QPlaceIdReply) -> PlaceIdReply:
        reply = cls(obj.operationType(), obj.parent())
        reply.setId(obj.id())
        return reply

    def get_operation_type(self) -> OperationTypeStr:
        """Get current operation_type.

        Returns:
            current operation_type
        """
        return OPERATION_TYPES.inverse[self.operationType()]


if __name__ == "__main__":
    reply = PlaceIdReply(QtLocation.QPlaceIdReply.OperationType.SavePlace)
