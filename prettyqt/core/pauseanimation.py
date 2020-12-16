from qtpy import QtCore

from prettyqt import core


QtCore.QPauseAnimation.__bases__ = (core.AbstractAnimation,)


class PauseAnimation(QtCore.QPauseAnimation):
    def __repr__(self):
        return f"{type(self).__name__}({self.duration()})"
