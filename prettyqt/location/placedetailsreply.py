from __future__ import annotations

from prettyqt import location
from prettyqt.qt import QtLocation


QtLocation.QPlaceDetailsReply.__bases__ = (location.PlaceReply,)


class PlaceDetailsReply(QtLocation.QPlaceDetailsReply):
    @classmethod
    def clone_from(cls, obj: QtLocation.QPlaceDetailsReply) -> PlaceDetailsReply:
        reply = cls(obj.parent())
        reply.setPlace(location.Place(obj.place()))
        return reply

    def get_place(self) -> location.Place:
        return location.Place(self.place())


if __name__ == "__main__":
    reply = PlaceDetailsReply()
    print(dir(reply))
