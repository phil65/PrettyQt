from qtpy import QtCore

from prettyqt import core


QtCore.QSequentialAnimationGroup.__bases__ = (core.AnimationGroup,)


class SequentialAnimationGroup(QtCore.QSequentialAnimationGroup):
    pass
