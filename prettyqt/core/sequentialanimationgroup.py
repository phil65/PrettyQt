from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class SequentialAnimationGroup(
    core.AnimationGroupMixin, QtCore.QSequentialAnimationGroup
):
    pass
