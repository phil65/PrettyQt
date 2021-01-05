from __future__ import annotations

from prettyqt import gui
from prettyqt.qt import QtGui


class FontInfo(QtGui.QFontInfo):
    def get_style_hint(self) -> gui.font.StyleHintStr:
        return gui.font.STYLE_HINTS.inverse[self.styleHint()]
