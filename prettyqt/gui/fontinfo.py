# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui

STYLE_HINTS = gui.font.STYLE_HINTS  # type: ignore


class FontInfo(QtGui.QFontInfo):
    def get_style_hint(self):
        return STYLE_HINTS.inv[self.styleHint()]
