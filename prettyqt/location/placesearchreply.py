# -*- coding: utf-8 -*-

from typing import List

from qtpy import QtLocation

from prettyqt import location


QtLocation.QPlaceSearchReply.__bases__ = (location.PlaceReply,)


class PlaceSearchReply(QtLocation.QPlaceSearchReply):
    def __iter__(self):
        return iter(self.get_results())

    def __getitem__(self, index: int):
        return self.get_results()[index]

    def __len__(self):
        return len(self.get_results())

    def get_results(self) -> List[location.PlaceSearchResult]:
        return [location.PlaceSearchResult(i) for i in self.results()]


if __name__ == "__main__":
    reply = PlaceSearchReply()
