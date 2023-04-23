from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import get_repr


class PauseAnimation(core.AbstractAnimationMixin, QtCore.QPauseAnimation):
    def __repr__(self):
        return get_repr(self, self.duration())
