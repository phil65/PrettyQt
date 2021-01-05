from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionFocusRect.__bases__ = (widgets.StyleOption,)


class StyleOptionFocusRect(QtWidgets.QStyleOptionFocusRect):
    pass
