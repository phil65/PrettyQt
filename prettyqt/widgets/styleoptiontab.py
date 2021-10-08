from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


CORNER_WIDGETS = bidict(
    none=QtWidgets.QStyleOptionTab.CornerWidget.NoCornerWidgets,
    left=QtWidgets.QStyleOptionTab.CornerWidget.LeftCornerWidget,
    right=QtWidgets.QStyleOptionTab.CornerWidget.RightCornerWidget,
)

SELECTED_POSITION = bidict(
    not_adjacent=QtWidgets.QStyleOptionTab.SelectedPosition.NotAdjacent,
    next_is_selected=QtWidgets.QStyleOptionTab.SelectedPosition.NextIsSelected,
    previous_is_selected=QtWidgets.QStyleOptionTab.SelectedPosition.PreviousIsSelected,
)

TAB_FEATURE = bidict(
    none=QtWidgets.QStyleOptionTab.TabFeature(0),  # type: ignore
    has_frame=QtWidgets.QStyleOptionTab.TabFeature.HasFrame,
)

TAB_POSITION = bidict(
    beginning=QtWidgets.QStyleOptionTab.TabPosition.Beginning,
    middle=QtWidgets.QStyleOptionTab.TabPosition.Middle,
    end=QtWidgets.QStyleOptionTab.TabPosition.End,
    only_one_tab=QtWidgets.QStyleOptionTab.TabPosition.OnlyOneTab,
)


QtWidgets.QStyleOptionTab.__bases__ = (widgets.StyleOption,)


class StyleOptionTab(QtWidgets.QStyleOptionTab):
    pass
