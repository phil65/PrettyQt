from __future__ import annotations

from prettyqt import location


class PlaceCategory(location.QPlaceCategory):
    """Represents a category that a QPlace can be associated with."""

    def __str__(self):
        return self.name()

    def __bool__(self):
        return not self.isEmpty()

    def get_icon(self) -> location.PlaceIcon | None:
        icon = self.icon()
        return None if icon.isEmpty() else location.PlaceIcon(icon)

    def get_visibility(self) -> location.VisibilityStr:
        """Return the visibility of the place.

        Returns:
            Visibility
        """
        return location.VISIBILITY.inverse[self.visibility()]


if __name__ == "__main__":
    category = PlaceCategory()
    print(bool(category))
