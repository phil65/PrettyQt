from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionGraphicsItem.__bases__ = (widgets.StyleOption,)


class StyleOptionGraphicsItem(QtWidgets.QStyleOptionGraphicsItem):
    pass
