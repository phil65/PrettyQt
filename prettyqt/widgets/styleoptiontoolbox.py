from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


mod = QtWidgets.QStyleOptionToolBox

SELECTED_POSITION = bidict(
    not_adjacent=mod.SelectedPosition.NotAdjacent,
    next_is_selected=mod.SelectedPosition.NextIsSelected,
    previous_is_selected=mod.SelectedPosition.PreviousIsSelected,
)

TAB_POSITION = bidict(
    beginning=mod.TabPosition.Beginning,
    middle=mod.TabPosition.Middle,
    end=mod.TabPosition.End,
    only_one_tab=mod.TabPosition.OnlyOneTab,
)


QtWidgets.QStyleOptionToolBox.__bases__ = (widgets.StyleOption,)


class StyleOptionToolBox(QtWidgets.QStyleOptionToolBox):
    pass
