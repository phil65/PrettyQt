from __future__ import annotations

from typing_extensions import Self

from prettyqt import location


class PlaceDetailsReply(location.PlaceReplyMixin, location.QPlaceDetailsReply):
    @classmethod
    def clone_from(cls, obj: location.QPlaceDetailsReply) -> Self:
        reply = cls(obj.parent())
        reply.setPlace(location.Place(obj.place()))
        return reply

    def get_place(self) -> location.Place:
        return location.Place(self.place())


if __name__ == "__main__":
    reply = PlaceDetailsReply()
    print(dir(reply))
