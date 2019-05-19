# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
    pass


SyntaxHighlighter.__bases__[0].__bases__ = (core.Object,)
