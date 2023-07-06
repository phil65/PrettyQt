from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, overload

from prettyqt import core
from prettyqt.utils import listdelegators


if TYPE_CHECKING:
    from prettyqt import widgets


class AnimationGroupMixin(core.AbstractAnimationMixin):
    @overload
    def __getitem__(self, index: int) -> core.QAbstractAnimation:
        ...

    @overload
    def __getitem__(
        self, index: slice
    ) -> listdelegators.ListDelegator[core.QAbstractAnimation]:
        ...

    def __getitem__(self, index: int | slice):
        count = self.animationCount()
        match index:
            case int():
                if index < 0:
                    index = count + index
                if index >= count:
                    raise IndexError(index)
                anim = self.animationAt(index)
                if anim is None:
                    raise KeyError(index)
                return anim
            case slice():
                stop = index.stop or count
                rng = range(index.start or 0, stop, index.step or 1)
                anims = [self.animationAt(i) for i in rng]
                return listdelegators.ListDelegator(anims)
            case _:
                raise TypeError(index)

    def __setitem__(self, index: int, value: core.QAbstractAnimation):
        if not (0 <= index < self.animationCount()):
            raise KeyError(index)
        self.takeAnimation(index)
        self.insertAnimation(index, value)

    def __len__(self):
        return self.animationCount()

    def __delitem__(self, index: int):
        if not (0 <= index < self.animationCount()):
            raise KeyError(index)
        self.takeAnimation(index)

    def __add__(self, other: core.QAbstractAnimation):
        self.addAnimation(other)
        return self

    def targetObject(self) -> widgets.QWidget:
        """Return shared targetObject if existing."""
        targets = [
            anim.targetObject()
            for i in range(self.animationCount())
            if isinstance((anim := self.animationAt(i)), core.QPropertyAnimation)
        ]
        if len(targets) != self.animationCount() or len(set(targets)) != 1:
            raise RuntimeError("Could not find shared targetObject for all animations.")
        return targets[0]

    def add_property_animation(self, obj: Callable) -> core.PropertyAnimation:
        anim = core.PropertyAnimation()
        anim.apply_to(obj)
        self.addAnimation(anim)
        return anim


class AnimationGroup(AnimationGroupMixin, core.QAnimationGroup):
    pass


if __name__ == "__main__":
    group = AnimationGroup()
    a1 = core.PauseAnimation()
    a2 = core.PauseAnimation()
    group += a1
    group += a2
    sliced = group[:2]
