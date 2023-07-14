from __future__ import annotations

from collections.abc import Iterator

from typing_extensions import Self

from prettyqt import location


class PlaceMatchReply(location.PlaceReplyMixin, location.QPlaceMatchReply):
    """Manages a place matching operation started by an instance of QPlaceManager."""

    def __iter__(self) -> Iterator[location.Place]:
        return iter(self.get_places())

    def __getitem__(self, index: int) -> location.Place:
        return self.get_places()[index]

    def __len__(self):
        return len(self.get_places())

    @classmethod
    def clone_from(cls, obj: location.QPlaceMatchReply) -> Self:
        reply = cls(obj.parent())
        reply.setPlaces([location.Place(i) for i in obj.places()])
        request = location.PlaceMatchRequest(obj.request())
        reply.setRequest(request)
        return reply

    def get_places(self) -> list[location.Place]:
        return [location.Place(i) for i in self.places()]

    def get_request(self) -> location.PlaceMatchRequest:
        return location.PlaceMatchRequest(self.request())


if __name__ == "__main__":
    reply = PlaceMatchReply()
