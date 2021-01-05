from __future__ import annotations

from prettyqt import constants, core
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


class FontMetrics(QtGui.QFontMetrics):
    def elided_text(
        self, text: str, mode: constants.ElideModeStr, width: int, flags=0
    ) -> str:
        if mode not in constants.ELIDE_MODE:
            raise InvalidParamError(mode, constants.ELIDE_MODE)
        return self.elidedText(text, constants.ELIDE_MODE[mode], width, flags)

    def get_bounding_rect(self, *args) -> core.Rect:
        return core.Rect(self.boundingRect(*args))

    def get_tight_bounding_rect(self, text: str) -> core.Rect:
        return core.Rect(self.tightBoundingRect(text))


if __name__ == "__main__":
    app = QtGui.QGuiApplication([])
    font = QtGui.QFont()
    metrics = FontMetrics(font)
    print(metrics.get_bounding_rect("test"))
