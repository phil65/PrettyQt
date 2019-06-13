# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QCoreApplication.__bases__ = (core.Object,)


class CoreApplication(QtCore.QCoreApplication):
    pass
