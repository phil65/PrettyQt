from qtpy import QtCore

from prettyqt import core


QtCore.QParallelAnimationGroup.__bases__ = (core.AnimationGroup,)


class ParallelAnimationGroup(QtCore.QParallelAnimationGroup):
    def set_duration(self, duration: int):
        anims = [self.animationAt(i) for i in range(len(self))]
        for anim in anims:
            anim.setDuration(duration)
