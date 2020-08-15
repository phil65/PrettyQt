# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core

QtCore.QAnimationGroup.__bases__ = (core.AbstractAnimation,)


class AnimationGroup(QtCore.QAnimationGroup):
    def __getitem__(self, index: int):
        return self.animationAt(index)

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
