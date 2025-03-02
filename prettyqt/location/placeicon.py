from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core
from prettyqt.qt import QtLocation


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class PlaceIcon(QtLocation.QPlaceIcon):
    """Represents an icon."""

    def __bool__(self):
        return not self.isEmpty()

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

    # def get_manager(self) -> location.PlaceManager:
    #     return location.PlaceManager(self.manager())

    def get_url(self) -> core.Url:
        return core.Url(self.url())


if __name__ == "__main__":
    icon = PlaceIcon()
    print(bool(icon))
