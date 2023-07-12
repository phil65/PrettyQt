from __future__ import annotations

from prettyqt import gui


class FontInfo(gui.QFontInfo):
    """General information about fonts."""

    def get_style_hint(self) -> gui.font.StyleHintStr:
        return gui.font.STYLE_HINTS.inverse[self.styleHint()]
