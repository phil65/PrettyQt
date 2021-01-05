from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionTitleBar.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionTitleBar(QtWidgets.QStyleOptionTitleBar):
    pass
