from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionToolButton.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionToolButton(QtWidgets.QStyleOptionToolButton):
    pass
