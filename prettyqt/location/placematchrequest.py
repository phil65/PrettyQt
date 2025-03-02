from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import location


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class PlaceMatchRequest(location.QPlaceMatchRequest):
    def __setitem__(self, index: str, val: datatypes.Variant):
        attrs = self.parameters()
        attrs[index] = val
        self.setParameters(attrs)

    def __getitem__(self, index: str) -> datatypes.Variant:
        attr = self.parameters()
        if index not in attr:
            msg = f"Key {index!r} does not exist."
            raise KeyError(msg)
        return attr[index]

    def get_places(self) -> list[location.Place]:
        return [location.Place(i) for i in self.places()]


if __name__ == "__main__":
    request = PlaceMatchRequest()
