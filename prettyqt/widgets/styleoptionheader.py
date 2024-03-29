from __future__ import annotations

from prettyqt import widgets
from prettyqt.utils import bidict


mod = widgets.QStyleOptionHeader

SECTION_POSITION = bidict(
    beginning=mod.SectionPosition.Beginning,
    middle=mod.SectionPosition.Middle,
    end=mod.SectionPosition.End,
    only_one_section=mod.SectionPosition.OnlyOneSection,
)

SELECTED_POSITION = bidict(
    not_adjacent=mod.SelectedPosition.NotAdjacent,
    next_is_selected=mod.SelectedPosition.NextIsSelected,
    previous_is_selected=mod.SelectedPosition.PreviousIsSelected,
    next_and_previous_are_selected=mod.SelectedPosition.NextAndPreviousAreSelected,
)

SORT_INDICATOR = bidict(
    none=mod.SortIndicator(0),  # type: ignore
    sort_up=mod.SortIndicator.SortUp,
    sort_down=mod.SortIndicator.SortDown,
)


class StyleOptionHeader(widgets.StyleOptionMixin, widgets.QStyleOptionHeader):
    pass
