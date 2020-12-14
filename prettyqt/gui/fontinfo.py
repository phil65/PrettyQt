from qtpy import QtGui

from prettyqt import gui


class FontInfo(QtGui.QFontInfo):
    def get_style_hint(self) -> gui.font.StyleHintStr:
        return gui.font.STYLE_HINTS.inverse[self.styleHint()]
