from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


CORNER_WIDGETS = bidict(
    none=QtWidgets.QStyleOptionTab.NoCornerWidgets,
    left=QtWidgets.QStyleOptionTab.LeftCornerWidget,
    right=QtWidgets.QStyleOptionTab.RightCornerWidget,
)

SELECTED_POSITION = bidict(
    not_adjacent=QtWidgets.QStyleOptionTab.NotAdjacent,
    next_is_selected=QtWidgets.QStyleOptionTab.NextIsSelected,
    previous_is_selected=QtWidgets.QStyleOptionTab.PreviousIsSelected,
)

TAB_FEATURE = bidict(
    none=QtWidgets.QStyleOptionTab.TabFeature(0),
    has_frame=QtWidgets.QStyleOptionTab.HasFrame,
)

TAB_POSITION = bidict(
    beginning=QtWidgets.QStyleOptionTab.Beginning,
    middle=QtWidgets.QStyleOptionTab.Middle,
    end=QtWidgets.QStyleOptionTab.End,
    only_one_tab=QtWidgets.QStyleOptionTab.OnlyOneTab,
)


QtWidgets.QStyleOptionTab.__bases__ = (widgets.StyleOption,)


class StyleOptionTab(QtWidgets.QStyleOptionTab):
    pass
