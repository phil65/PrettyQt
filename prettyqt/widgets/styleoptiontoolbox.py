from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


mod = QtWidgets.QStyleOptionToolBox

SELECTED_POSITION = bidict(
    not_adjacent=mod.SelectedPosition.NotAdjacent,
    next_is_selected=mod.SelectedPosition.NextIsSelected,
    previous_is_selected=mod.SelectedPosition.PreviousIsSelected,
)

SelectedPositionStr = Literal["not_adjacent", "next_is_selected", "previous_is_selected"]

TAB_POSITION = bidict(
    beginning=mod.TabPosition.Beginning,
    middle=mod.TabPosition.Middle,
    end=mod.TabPosition.End,
    only_one_tab=mod.TabPosition.OnlyOneTab,
)

TabPositionStr = Literal["beginning", "middle", "end" "only_one_tab"]


QtWidgets.QStyleOptionToolBox.__bases__ = (widgets.StyleOption,)


class StyleOptionToolBox(QtWidgets.QStyleOptionToolBox):
    def set_selected_position(self, position: SelectedPositionStr):
        self.selectedPosition = SELECTED_POSITION[position]

    def get_selected_position(self) -> SelectedPositionStr:
        return SELECTED_POSITION.inv[self.selectedPosition]


if __name__ == "__main__":
    opt = StyleOptionToolBox()
    print(opt.get_selected_position())
