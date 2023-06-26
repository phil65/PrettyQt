from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui


class FontMetricsF(QtGui.QFontMetricsF):
    def elided_text(
        self,
        text: str,
        mode: constants.TextElideModeStr | constants.TextElideMode,
        width: float,
        flags=0,
    ) -> str:
        val = constants.TEXT_ELIDE_MODE.get_enum_value(mode)
        return self.elidedText(text, val, width, flags)

    def get_bounding_rect(self, *args) -> core.RectF:
        return core.RectF(self.boundingRect(*args))

    def get_tight_bounding_rect(self, text: str) -> core.RectF:
        return core.RectF(self.tightBoundingRect(text))
