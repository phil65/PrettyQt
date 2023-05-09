from __future__ import annotations

from prettyqt.qt import QtCore


class Property(QtCore.Property):
    pass


if __name__ == "__main__":
    prop = Property(int)
