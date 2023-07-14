from __future__ import annotations

from prettyqt.qt import QtLocation


class PlaceUser(QtLocation.QPlaceUser):
    """Represents an individual user."""

    def __str__(self):
        return self.name()


if __name__ == "__main__":
    user = PlaceUser()
