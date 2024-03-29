from __future__ import annotations

from prettyqt.qt import QtCore


class PersistentModelIndex(QtCore.QPersistentModelIndex):
    """Used to locate data in a data model."""

    def __bool__(self):
        return self.isValid()

    def __getitem__(self, flag: int):
        return self.data(flag)


if __name__ == "__main__":
    index = PersistentModelIndex()
