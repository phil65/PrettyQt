from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class ParallelAnimationGroup(core.AnimationGroupMixin, QtCore.QParallelAnimationGroup):
    def set_duration(self, duration: int):
        for anim in self:
            match anim:
                # I dont think we need to support nested Animations here..
                case core.QVariantAnimation():
                    anim.setDuration(duration)
                case _:
                    raise TypeError("set_duration only works with QVariantAnimations.")
