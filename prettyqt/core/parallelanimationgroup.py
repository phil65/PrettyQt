# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core

QtCore.QParallelAnimationGroup.__bases__ = (core.AnimationGroup,)


class ParallelAnimationGroup(QtCore.QParallelAnimationGroup):
    pass
