from typing import Literal

from qtpy import QtCore, QtGui

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


ELIDE_MODE = bidict(
    left=QtCore.Qt.ElideLeft,
    right=QtCore.Qt.ElideRight,
    middle=QtCore.Qt.ElideMiddle,
    none=QtCore.Qt.ElideNone,
)

ElideModeStr = Literal["left", "right", "middle", "none"]


class FontMetrics(QtGui.QFontMetrics):
    def elided_text(self, text: str, mode: ElideModeStr, width: int, flags=0) -> str:
        if mode not in ELIDE_MODE:
            raise InvalidParamError(mode, ELIDE_MODE)
        return self.elidedText(text, ELIDE_MODE[mode], width, flags)

    def get_bounding_rect(self, *args, **kwargs) -> core.Rect:
        return core.Rect(self.boundingRect(*args, **kwargs))

    def get_tight_bounding_rect(self, text: str) -> core.Rect:
        return core.Rect(self.tightBoundingRect(text))
