from __future__ import annotations

from typing import overload

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import types


QtCore.QAnimationGroup.__bases__ = (core.AbstractAnimation,)


class AnimationGroup(QtCore.QAnimationGroup):
    @overload
    def __getitem__(self, index: int) -> QtCore.QAbstractAnimation:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[QtCore.QAbstractAnimation]:
        ...

    def __getitem__(self, index: int | slice):
        if isinstance(index, int):
            if index < 0:
                index = self.animationCount() + index
            anim = self.animationAt(index)
            if anim is None:
                raise KeyError(index)
            return anim
        else:
            anims = [self.animationAt(i) for i in range(len(self))]
            return anims[index]

    def __setitem__(self, index: int, value: QtCore.QAbstractAnimation):
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

    def __add__(self, other: QtCore.QAbstractAnimation):
        self.addAnimation(other)
        return self

    def add_property_animation(
        self, obj: QtCore.QObject, attribute: types.ByteArrayType
    ) -> core.PropertyAnimation:
        if isinstance(attribute, str):
            attribute = attribute.encode()
        if isinstance(attribute, bytes):
            attribute = QtCore.QByteArray(attribute)
        anim = core.PropertyAnimation(obj, attribute)
        self.addAnimation(anim)
        return anim


if __name__ == "__main__":
    group = AnimationGroup()
    a1 = core.PauseAnimation()
    a2 = core.PauseAnimation()
    group += a1
    group += a2
    sliced = group[0:2]
