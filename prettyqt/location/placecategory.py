from __future__ import annotations

from typing import Optional

from prettyqt import location
from prettyqt.qt import QtLocation


class PlaceCategory(QtLocation.QPlaceCategory):
    def __str__(self):
        return self.name()

    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> Optional[location.PlaceIcon]:
        icon = self.icon()
        if icon.isEmpty():
            return None
        return location.PlaceIcon(icon)

    def get_visibility(self) -> location.VisibilityStr:
        """Return the visibility of the place.

        Returns:
            Visibility
        """
        return location.VISIBILITY.inverse[self.visibility()]


if __name__ == "__main__":
    category = PlaceCategory()
    print(bool(category))
