# -*- coding: utf-8 -*-

from typing import List

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceMatchReply.__bases__ = (location.PlaceReply,)


class PlaceMatchReply(QtLocation.QPlaceMatchReply):
    def __iter__(self):
        return iter(self.get_places())

    def __getitem__(self, index: int):
        return self.get_places()[index]

    def __len__(self):
        return len(self.get_places())

    def get_places(self) -> List[location.Place]:
        return [location.Place(i) for i in self.places()]

    def get_request(self) -> location.PlaceMatchRequest:
        return location.PlaceMatchRequest(self.request())


if __name__ == "__main__":
    reply = PlaceMatchReply()
