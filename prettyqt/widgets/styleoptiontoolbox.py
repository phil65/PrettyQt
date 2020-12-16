from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


SELECTED_POSITION = bidict(
    not_adjacent=QtWidgets.QStyleOptionToolBox.NotAdjacent,
    next_is_selected=QtWidgets.QStyleOptionToolBox.NextIsSelected,
    previous_is_selected=QtWidgets.QStyleOptionToolBox.PreviousIsSelected,
)

TAB_POSITION = bidict(
    beginning=QtWidgets.QStyleOptionToolBox.Beginning,
    middle=QtWidgets.QStyleOptionToolBox.Middle,
    end=QtWidgets.QStyleOptionToolBox.End,
    only_one_tab=QtWidgets.QStyleOptionToolBox.OnlyOneTab,
)


QtWidgets.QStyleOptionToolBox.__bases__ = (widgets.StyleOption,)


class StyleOptionToolBox(QtWidgets.QStyleOptionToolBox):
    pass
