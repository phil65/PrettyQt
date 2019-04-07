# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtGui
from prettyqt import gui, core


class YamlHighlighter(QtGui.QSyntaxHighlighter):
    """
    Enabled the syntax highlightning for the yaml files.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        self.commentStart = core.RegExp("#")
        self.commentEnd = core.RegExp("\n|\r")
        self.commentFormat = gui.TextCharFormat()
        self.commentFormat.setFontItalic(True)
        self.commentFormat.setForeground(QtCore.Qt.darkGray)
        f = gui.TextCharFormat()
        r = core.RegExp()
        r.setMinimal(True)
        f.setFontWeight(QtGui.QFont.Normal)
        f.setForeground(QtCore.Qt.blue)
        tag_list = ["\\btrue\\b", "\\bfalse\\b"]
        for tag in tag_list:
            r.setPattern(tag)
            self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(gui.Color(127, 64, 127))
        r.setPattern("\\d+")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(QtCore.Qt.darkBlue)
        r.setPattern("^\s*[_.\w]*\s*:")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(QtCore.Qt.darkBlue)
        r.setPattern(":\s*:[_\.\w]*$|:\s*\@[_\.\w]*$")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setFontWeight(QtGui.QFont.Bold)
        f.setForeground(QtCore.Qt.darkRed)
        r.setPattern("^\s*-")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(QtCore.Qt.darkRed)
        r.setPattern("^---$")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(QtCore.Qt.darkGreen)
        r.setPattern("[\[\]\{\}\,]")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setFontWeight(QtGui.QFont.Normal)
        f.setForeground(QtCore.Qt.magenta)
        r.setPattern("\".*\"|\'.*\'")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(gui.Color(127, 64, 127))
        r.setPattern("\\$\\(.*\\)")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        f.setForeground(QtCore.Qt.lightGray)
        r.setPattern("<!DOCTYPE.*>")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
        r.setPattern("<\\?xml.*\\?>")
        self.rules.append((core.RegExp(r), gui.TextCharFormat(f)))
