from prettyqt import core


class SequentialAnimationGroup(core.AnimationGroupMixin, core.QSequentialAnimationGroup):
    """Sequential group of animations."""

    def reverse(self):
        """Reverse animation in-place by switching start and end values."""
        for anim in reversed(list(self)):
            if not isinstance(anim, core.QVariantAnimation):
                continue
            old_start = anim.startValue()
            old_end = anim.endValue()
            anim.setStartValue(old_end)
            anim.setEndValue(old_start)

    def reversed(self) -> SequentialAnimationGroup:
        """Return a reversed copy of the animation."""
        new = core.MetaObject(self.metaObject()).copy(self)
        for anim in reversed(list(self)):
            if not isinstance(
                anim, core.VariantAnimationMixin | SequentialAnimationGroup
            ):
                raise TypeError(anim)
            new.addAnimation(anim.reversed())
        return new

    def append_reversed(self) -> core.SequentialAnimationGroup:
        """Return copy of animation with appended reverse animation."""
        revers = self.reversed()
        animation = core.SequentialAnimationGroup()
        animation.addAnimation(self)
        animation.addAnimation(revers)
        return animation
