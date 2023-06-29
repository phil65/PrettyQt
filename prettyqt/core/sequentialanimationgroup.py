from __future__ import annotations

from prettyqt import core


class SequentialAnimationGroup(core.AnimationGroupMixin, core.QSequentialAnimationGroup):
    def reverse(self):
        for anim in reversed(list(self)):
            old_start = anim.startValue()
            old_end = anim.endValue()
            anim.setStartValue(old_end)
            anim.setEndValue(old_start)

    def reversed(self) -> SequentialAnimationGroup:
        new = core.MetaObject(self.metaObject()).copy(self)
        for anim in reversed(list(self)):
            animation = core.MetaObject(anim.get_metaobject()).copy(anim)
            animation = animation.reversed()
            new.addAnimation(animation)
        return new

    def append_reversed(self) -> core.SequentialAnimationGroup:
        revers = self.reversed()
        animation = core.SequentialAnimationGroup()
        animation.addAnimation(self)
        animation.addAnimation(revers)
        return animation
