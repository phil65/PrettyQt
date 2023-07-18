from __future__ import annotations

from prettyqt.qt import QtCore


class Property(QtCore.Property):
    """Template class that enables automatic property bindings."""


if __name__ == "__main__":
    prop = Property(int)
