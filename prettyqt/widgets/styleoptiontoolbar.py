from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


ToolBarFeatureStr = Literal["none", "movable"]

TOOLBAR_FEATURE: bidict[ToolBarFeatureStr, widgets.QStyleOptionToolBar.ToolBarFeature] = (
    bidict(
        none=widgets.QStyleOptionToolBar.ToolBarFeature(0),  # type: ignore
        movable=widgets.QStyleOptionToolBar.ToolBarFeature.Movable,
    )
)


class StyleOptionToolBar(widgets.StyleOptionMixin, widgets.QStyleOptionToolBar):
    pass
