from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionButton.__bases__ = (widgets.StyleOption,)


class StyleOptionButton(QtWidgets.QStyleOptionButton):
    pass
