from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QPauseAnimation.__bases__ = (core.AbstractAnimation,)


class PauseAnimation(QtCore.QPauseAnimation):
    def __repr__(self):
        return f"{type(self).__name__}({self.duration()})"
