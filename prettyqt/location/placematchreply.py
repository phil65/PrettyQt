from __future__ import annotations

from typing import Iterator, List

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceMatchReply.__bases__ = (location.PlaceReply,)


class PlaceMatchReply(QtLocation.QPlaceMatchReply):
    def __iter__(self) -> Iterator[location.Place]:
        return iter(self.get_places())

    def __getitem__(self, index: int) -> location.Place:
        return self.get_places()[index]

    def __len__(self):
        return len(self.get_places())

    @classmethod
    def clone_from(cls, obj: QtLocation.QPlaceMatchReply) -> PlaceMatchReply:
        reply = cls(obj.parent())
        reply.setPlaces([location.Place(i) for i in obj.places()])
        request = location.PlaceMatchRequest(obj.request())
        reply.setRequest(request)
        return reply

    def get_places(self) -> List[location.Place]:
        return [location.Place(i) for i in self.places()]

    def get_request(self) -> location.PlaceMatchRequest:
        return location.PlaceMatchRequest(self.request())


if __name__ == "__main__":
    reply = PlaceMatchReply()
