from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


CornerWidgetStr = Literal["none", "left", "right"]

CORNER_WIDGETS: bidict[CornerWidgetStr, widgets.QStyleOptionTab.CornerWidget] = bidict(
    none=widgets.QStyleOptionTab.CornerWidget.NoCornerWidgets,
    left=widgets.QStyleOptionTab.CornerWidget.LeftCornerWidget,
    right=widgets.QStyleOptionTab.CornerWidget.RightCornerWidget,
)

SelectedPositionStr = Literal["not_adjacent", "next_is_selected", "previous_is_selected"]

SELECTED_POSITION: bidict[
    SelectedPositionStr, widgets.QStyleOptionTab.SelectedPosition
] = bidict(
    not_adjacent=widgets.QStyleOptionTab.SelectedPosition.NotAdjacent,
    next_is_selected=widgets.QStyleOptionTab.SelectedPosition.NextIsSelected,
    previous_is_selected=widgets.QStyleOptionTab.SelectedPosition.PreviousIsSelected,
)

TabFeatureStr = Literal["none", "has_frame", "minimum_size_hint"]

TAB_FEATURE: bidict[TabFeatureStr, widgets.QStyleOptionTab.TabFeature] = bidict(
    none=widgets.QStyleOptionTab.TabFeature(0),
    has_frame=widgets.QStyleOptionTab.TabFeature.HasFrame,
    minimum_size_hint=widgets.QStyleOptionTab.TabFeature.MinimumSizeHint,
)

TabPositionStr = Literal["beginning", "middle", "end", "only_one_tab", "moving"]

TAB_POSITION: bidict[TabPositionStr, widgets.QStyleOptionTab.TabPosition] = bidict(
    beginning=widgets.QStyleOptionTab.TabPosition.Beginning,
    middle=widgets.QStyleOptionTab.TabPosition.Middle,
    end=widgets.QStyleOptionTab.TabPosition.End,
    only_one_tab=widgets.QStyleOptionTab.TabPosition.OnlyOneTab,
    moving=widgets.QStyleOptionTab.TabPosition.Moving,
)


class StyleOptionTab(widgets.StyleOptionMixin, widgets.QStyleOptionTab):
    pass
