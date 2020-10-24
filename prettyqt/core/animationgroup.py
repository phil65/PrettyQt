# -*- coding: utf-8 -*-

from typing import Union

from qtpy import QtCore

from prettyqt import core

QtCore.QAnimationGroup.__bases__ = (core.AbstractAnimation,)


class AnimationGroup(QtCore.QAnimationGroup):
    def __getitem__(self, index: Union[int, slice]):
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index
            return self.animationAt(index)
        else:
            anims = [self.animationAt(i) for i in range(len(self))]
            return anims[index]

    def __setitem__(self, index: int, value: QtCore.QAbstractAnimation):
        old = self.animationAt(index)
        self.removeAnimation(old)
        self.insertAnimation(index, value)

    def __len__(self):
        return self.animationCount()

    def __delitem__(self, index: int):
        animation = self[index]
        self.removeAnimation(animation)

    def __add__(self, other: QtCore.QAbstractAnimation):
        self.addAnimation(other)
        return self

    def add_property_animation(
        self, obj: QtCore.QObject, attribute: str
    ) -> core.PropertyAnimation:
        anim = core.PropertyAnimation(obj, attribute.encode())
        self.addAnimation(anim)
        return anim
