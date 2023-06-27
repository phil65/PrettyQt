from __future__ import annotations

from prettyqt import gui


class FontInfo(gui.QFontInfo):
    def get_style_hint(self) -> gui.font.StyleHintStr:
        return gui.font.STYLE_HINTS.inverse[self.styleHint()]
