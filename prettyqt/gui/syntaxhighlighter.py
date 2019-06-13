# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui

from prettyqt import core


QtGui.QSyntaxHighlighter.__bases__ = (core.Object,)


class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
    pass
