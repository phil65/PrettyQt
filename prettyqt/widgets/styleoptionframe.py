from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionFrame.__bases__ = (widgets.StyleOption,)


class StyleOptionFrame(QtWidgets.QStyleOptionFrame):
    pass
