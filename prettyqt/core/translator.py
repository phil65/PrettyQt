# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core


QtCore.QTranslator.__bases__ = (core.Object,)


class Translator(QtCore.QTranslator):
    pass
