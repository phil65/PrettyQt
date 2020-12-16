from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict


QStyleOptionHeader = QtWidgets.QStyleOptionHeader

SECTION_POSITION = bidict(
    beginning=QtWidgets.QStyleOptionHeader.Beginning,
    middle=QtWidgets.QStyleOptionHeader.Middle,
    end=QtWidgets.QStyleOptionHeader.End,
    only_one_section=QtWidgets.QStyleOptionHeader.OnlyOneSection,
)

SELECTED_POSITION = bidict(
    not_adjacent=QStyleOptionHeader.NotAdjacent,
    next_is_selected=QStyleOptionHeader.NextIsSelected,
    previous_is_selected=QStyleOptionHeader.PreviousIsSelected,
    next_and_previous_are_selected=QStyleOptionHeader.NextAndPreviousAreSelected,
)

SORT_INDICATOR = bidict(
    none=QtWidgets.QStyleOptionHeader.SortIndicator(0),
    sort_up=QtWidgets.QStyleOptionHeader.SortUp,
    sort_down=QtWidgets.QStyleOptionHeader.SortDown,
)


QtWidgets.QStyleOptionHeader.__bases__ = (widgets.StyleOption,)


class StyleOptionHeader(QtWidgets.QStyleOptionHeader):
    pass
