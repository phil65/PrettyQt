# -*- coding: utf-8 -*-

from qtpy import QtLocation

from prettyqt import location
from prettyqt.utils import bidict


OPERATION_TYPES = bidict(
    save_place=QtLocation.QPlaceIdReply.SavePlace,
    remove_place=QtLocation.QPlaceIdReply.RemovePlace,
    save_category=QtLocation.QPlaceIdReply.SaveCategory,
    remove_category=QtLocation.QPlaceIdReply.RemoveCategory,
)

QtLocation.QPlaceIdReply.__bases__ = (location.PlaceReply,)


class PlaceIdReply(QtLocation.QPlaceIdReply):
    def __repr__(self):
        return f"PlaceIdReply({self.operationType()})"

    def get_operation_type(self) -> str:
        """Get current operation_type.

        Possible values: "save_place", "remove_place", save_category", "remove_category"

        Returns:
            current operation_type
        """
        return OPERATION_TYPES.inv[self.operationType()]


if __name__ == "__main__":
    reply = PlaceIdReply(0)
