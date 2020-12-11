from qtpy import QtCore, QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


ELIDE_MODES = bidict(
    left=QtCore.Qt.ElideLeft,
    right=QtCore.Qt.ElideRight,
    middle=QtCore.Qt.ElideMiddle,
    none=QtCore.Qt.ElideNone,
)


class FontMetricsF(QtGui.QFontMetricsF):
    def elided_text(self, text: str, mode: str, width: float, flags=0) -> str:
        if mode not in ELIDE_MODES:
            raise InvalidParamError(mode, ELIDE_MODES)
        return self.elidedText(text, ELIDE_MODES[mode], width, flags)

    def get_bounding_rect(self, *args, **kwargs) -> core.RectF:
        return core.RectF(self.boundingRect(*args, **kwargs))

    def get_tight_bounding_rect(self, text: str) -> core.RectF:
        return core.RectF(self.tightBoundingRect(text))
