from qtpy import QtGui

from prettyqt import constants, core
from prettyqt.utils import InvalidParamError


class FontMetricsF(QtGui.QFontMetricsF):
    def elided_text(
        self, text: str, mode: constants.ElideModeStr, width: float, flags=0
    ) -> str:
        if mode not in constants.ELIDE_MODE:
            raise InvalidParamError(mode, constants.ELIDE_MODE)
        return self.elidedText(text, constants.ELIDE_MODE[mode], width, flags)

    def get_bounding_rect(self, *args, **kwargs) -> core.RectF:
        return core.RectF(self.boundingRect(*args, **kwargs))

    def get_tight_bounding_rect(self, text: str) -> core.RectF:
        return core.RectF(self.tightBoundingRect(text))
