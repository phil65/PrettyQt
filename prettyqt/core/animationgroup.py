from typing import List, overload

from qtpy import QtCore

from prettyqt import core


QtCore.QAnimationGroup.__bases__ = (core.AbstractAnimation,)


class AnimationGroup(QtCore.QAnimationGroup):
    @overload
    def __getitem__(self, index: int) -> QtCore.QAbstractAnimation:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[QtCore.QAbstractAnimation]:
        ...

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index
            return self.animationAt(index)
        else:
            anims = [self.animationAt(i) for i in range(len(self))]
            return anims[index]

    def __setitem__(self, index: int, value: QtCore.QAbstractAnimation):
        self.takeAnimation(index)
        self.insertAnimation(index, value)

    def __len__(self):
        return self.animationCount()

    def __delitem__(self, index: int):
        self.takeAnimation(index)

    def __add__(self, other: QtCore.QAbstractAnimation):
        self.addAnimation(other)
        return self

    def add_property_animation(
        self, obj: QtCore.QObject, attribute: str
    ) -> core.PropertyAnimation:
        anim = core.PropertyAnimation(obj, attribute.encode())
        self.addAnimation(anim)
        return anim


if __name__ == "__main__":
    group = AnimationGroup()
    a1 = core.PauseAnimation()
    a2 = core.PauseAnimation()
    group += a1
    group += a2
    sliced = group[0:2]
