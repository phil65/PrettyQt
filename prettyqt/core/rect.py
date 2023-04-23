from __future__ import annotations

from prettyqt.qt import QtCore
from prettyqt.utils import datatypes, get_repr


class Rect(QtCore.QRect):
    def __repr__(self):
        return get_repr(self, self.x(), self.y(), self.width(), self.height())

    def __reduce__(self):
        return type(self), (self.x(), self.y(), self.width(), self.height())

    def margins_added(self, margins: datatypes.MarginsType) -> Rect:
        if isinstance(margins, tuple):
            margins = QtCore.QMargins(*margins)
        return Rect(self.marginsAdded(margins))

    def margins_removed(self, margins: datatypes.MarginsType) -> Rect:
        if isinstance(margins, tuple):
            margins = QtCore.QMargins(*margins)
        return Rect(self.marginsRemoved(margins))


if __name__ == "__main__":
    rect = Rect(0, 2, 5, 5)
    print(repr(rect))
