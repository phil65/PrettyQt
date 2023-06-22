from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


ToolBarFeatureStr = Literal["none", "movable"]

TOOLBAR_FEATURE: bidict[
    ToolBarFeatureStr, QtWidgets.QStyleOptionToolBar.ToolBarFeature
] = bidict(
    none=QtWidgets.QStyleOptionToolBar.ToolBarFeature(0),  # type: ignore
    movable=QtWidgets.QStyleOptionToolBar.ToolBarFeature.Movable,
)


class StyleOptionToolBar(widgets.StyleOptionMixin, QtWidgets.QStyleOptionToolBar):
    pass
