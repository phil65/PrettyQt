from __future__ import annotations

from typing import List

from prettyqt import location
from prettyqt.qt import QtLocation
from prettyqt.utils import types


class PlaceMatchRequest(QtLocation.QPlaceMatchRequest):
    def __setitem__(self, index: str, val: types.Variant):
        attrs = self.parameters()
        attrs[index] = val
        self.setParameters(attrs)

    def __getitem__(self, index: str) -> types.Variant:
        attr = self.parameters()
        if index not in attr:
            raise KeyError(f"Key {index!r} does not exist.")
        return attr[index]

    def get_places(self) -> List[location.Place]:
        return [location.Place(i) for i in self.places()]


if __name__ == "__main__":
    request = PlaceMatchRequest()
