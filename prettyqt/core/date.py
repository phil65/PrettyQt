from __future__ import annotations

from prettyqt.qt import QtCore


class Date(QtCore.QDate):
    def __repr__(self):
        template = super().__repr__().split("(")[1]  # type: ignore
        return f"{type(self).__name__}({template}"

    def __str__(self):
        return self.toString("yyyy-MM-dd")

    def __reduce__(self):
        return type(self), (self.year(), self.month(), self.day())


if __name__ == "__main__":
    dt = Date(2000, 11, 11)
    print(dt)
