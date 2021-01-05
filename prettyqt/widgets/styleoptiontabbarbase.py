from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionTabBarBase.__bases__ = (widgets.StyleOption,)


class StyleOptionTabBarBase(QtWidgets.QStyleOptionTabBarBase):
    pass
