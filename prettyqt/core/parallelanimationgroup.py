from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QParallelAnimationGroup.__bases__ = (core.AnimationGroup,)


class ParallelAnimationGroup(QtCore.QParallelAnimationGroup):
    def set_duration(self, duration: int):
        anims = [self.animationAt(i) for i in range(len(self))]
        for anim in anims:
            anim.setDuration(duration)
