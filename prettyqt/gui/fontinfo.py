# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt import gui


class FontInfo(QtGui.QFontInfo):
    def get_style_hint(self):
        return gui.font.STYLE_HINTS.inv[self.styleHint()]
