from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


TOOLBAR_FEATURE = bidict(
    none=QtWidgets.QStyleOptionToolBar.ToolBarFeature(0),  # type: ignore
    movable=QtWidgets.QStyleOptionToolBar.ToolBarFeature.Movable,
)


class StyleOptionToolBar(widgets.StyleOptionMixin, QtWidgets.QStyleOptionToolBar):
    pass
