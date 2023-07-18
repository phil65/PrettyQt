from __future__ import annotations

from prettyqt import core


class SequentialAnimationGroup(core.AnimationGroupMixin, core.QSequentialAnimationGroup):
    """Sequential group of animations."""

    def reverse(self):
        """Reverse animation in-place by switching start and end values."""
        for anim in reversed(list(self)):
            old_start = anim.startValue()
            old_end = anim.endValue()
            anim.setStartValue(old_end)
            anim.setEndValue(old_start)

    def reversed(self) -> SequentialAnimationGroup:
        """Return a reversed copy of the animation."""
        new = core.MetaObject(self.metaObject()).copy(self)
        for anim in reversed(list(self)):
            animation = core.MetaObject(anim.get_metaobject()).copy(anim)
            animation = animation.reversed()
            new.addAnimation(animation)
        return new

    def append_reversed(self) -> core.SequentialAnimationGroup:
        """Return copy of animation with appended reverse animation."""
        revers = self.reversed()
        animation = core.SequentialAnimationGroup()
        animation.addAnimation(self)
        animation.addAnimation(revers)
        return animation
