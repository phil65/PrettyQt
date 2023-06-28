from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


CORNER_WIDGETS = bidict(
    none=widgets.QStyleOptionTab.CornerWidget.NoCornerWidgets,
    left=widgets.QStyleOptionTab.CornerWidget.LeftCornerWidget,
    right=widgets.QStyleOptionTab.CornerWidget.RightCornerWidget,
)

SELECTED_POSITION = bidict(
    not_adjacent=widgets.QStyleOptionTab.SelectedPosition.NotAdjacent,
    next_is_selected=widgets.QStyleOptionTab.SelectedPosition.NextIsSelected,
    previous_is_selected=widgets.QStyleOptionTab.SelectedPosition.PreviousIsSelected,
)

TAB_FEATURE = bidict(
    none=widgets.QStyleOptionTab.TabFeature(0),  # type: ignore
    has_frame=widgets.QStyleOptionTab.TabFeature.HasFrame,
)

TAB_POSITION = bidict(
    beginning=widgets.QStyleOptionTab.TabPosition.Beginning,
    middle=widgets.QStyleOptionTab.TabPosition.Middle,
    end=widgets.QStyleOptionTab.TabPosition.End,
    only_one_tab=widgets.QStyleOptionTab.TabPosition.OnlyOneTab,
)


class StyleOptionTab(widgets.StyleOptionMixin, widgets.QStyleOptionTab):
    pass
