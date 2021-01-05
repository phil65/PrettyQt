from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


TOOLBAR_FEATURE = bidict(
    none=QtWidgets.QStyleOptionToolBar.ToolBarFeature(),
    movable=QtWidgets.QStyleOptionToolBar.Movable,
)

QtWidgets.QStyleOptionToolBar.__bases__ = (widgets.StyleOption,)


class StyleOptionToolBar(QtWidgets.QStyleOptionToolBar):
    pass
