# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore
from prettyqt.utils import bidict

ELIDE_MODES = bidict(left=QtCore.Qt.ElideLeft,
                     right=QtCore.Qt.ElideRight,
                     middle=QtCore.Qt.ElideMiddle,
                     none=QtCore.Qt.ElideNone)


class FontMetrics(QtGui.QFontMetrics):

    def elided_text(self, text: str, mode: str, width: int, flags=0) -> str:
        if mode not in ELIDE_MODES:
            raise ValueError("Mode not available")
        return self.elidedText(text, ELIDE_MODES[mode], width, flags)
