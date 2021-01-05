from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QSequentialAnimationGroup.__bases__ = (core.AnimationGroup,)


class SequentialAnimationGroup(QtCore.QSequentialAnimationGroup):
    pass
