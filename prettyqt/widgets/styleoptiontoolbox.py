from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict


mod = widgets.QStyleOptionToolBox


SelectedPositionStr = Literal["not_adjacent", "next_is_selected", "previous_is_selected"]

SELECTED_POSITION: bidict[SelectedPositionStr, mod.SelectedPosition] = bidict(
    not_adjacent=mod.SelectedPosition.NotAdjacent,
    next_is_selected=mod.SelectedPosition.NextIsSelected,
    previous_is_selected=mod.SelectedPosition.PreviousIsSelected,
)


TabPositionStr = Literal["beginning", "middle", "end", "only_one_tab"]

TAB_POSITION: bidict[TabPositionStr, mod.TabPosition] = bidict(
    beginning=mod.TabPosition.Beginning,
    middle=mod.TabPosition.Middle,
    end=mod.TabPosition.End,
    only_one_tab=mod.TabPosition.OnlyOneTab,
)


class StyleOptionToolBox(widgets.StyleOptionMixin, widgets.QStyleOptionToolBox):
    def set_selected_position(self, position: SelectedPositionStr):
        self.selectedPosition = SELECTED_POSITION[position]

    def get_selected_position(self) -> SelectedPositionStr:
        return SELECTED_POSITION.inverse[self.selectedPosition]


if __name__ == "__main__":
    opt = StyleOptionToolBox()
