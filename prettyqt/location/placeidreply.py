from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt import location
from prettyqt.utils import bidict, get_repr


OPERATION_TYPES = bidict(
    save_place=location.QPlaceIdReply.OperationType.SavePlace,
    remove_place=location.QPlaceIdReply.OperationType.RemovePlace,
    save_category=location.QPlaceIdReply.OperationType.SaveCategory,
    remove_category=location.QPlaceIdReply.OperationType.RemoveCategory,
)

OperationTypeStr = Literal[
    "save_place", "remove_place", "save_category", "remove_category"
]


class PlaceIdReply(location.PlaceReplyMixin, location.QPlaceIdReply):
    """Manages saving and removal operations of places and categories."""

    def __repr__(self):
        return get_repr(self, self.operationType())

    @classmethod
    def clone_from(cls, obj: location.QPlaceIdReply) -> Self:
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
    reply = PlaceIdReply(location.QPlaceIdReply.OperationType.SavePlace)
