from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui


class FontMetrics(QtGui.QFontMetrics):
    """Font metrics information."""

    def elided_text(
        self,
        text: str,
        mode: constants.TextElideModeStr | constants.TextElideMode,
        width: int,
        flags=0,
    ) -> str:
        val = constants.TEXT_ELIDE_MODE.get_enum_value(mode)
        return self.elidedText(text, val, width, flags)

    def get_bounding_rect(self, *args) -> core.Rect:
        return core.Rect(self.boundingRect(*args))

    def get_tight_bounding_rect(self, text: str) -> core.Rect:
        return core.Rect(self.tightBoundingRect(text))


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    font = gui.Font()
    metrics = FontMetrics(font)
