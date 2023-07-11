from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


SelectionFlagStr = Literal[
    "none",
    "clear",
    "select",
    "deselect",
    "toggle",
    "current",
    "rows",
    "columns",
    "select_current",
    "toggle_current",
    "clear_and_select",
]

SELECTION_FLAG: bidict[SelectionFlagStr, core.QItemSelectionModel.SelectionFlag] = bidict(
    none=core.QItemSelectionModel.SelectionFlag.NoUpdate,
    clear=core.QItemSelectionModel.SelectionFlag.Clear,
    select=core.QItemSelectionModel.SelectionFlag.Select,
    deselect=core.QItemSelectionModel.SelectionFlag.Deselect,
    toggle=core.QItemSelectionModel.SelectionFlag.Toggle,
    current=core.QItemSelectionModel.SelectionFlag.Current,
    rows=core.QItemSelectionModel.SelectionFlag.Rows,
    columns=core.QItemSelectionModel.SelectionFlag.Columns,
    select_current=core.QItemSelectionModel.SelectionFlag.SelectCurrent,
    toggle_current=core.QItemSelectionModel.SelectionFlag.ToggleCurrent,
    clear_and_select=core.QItemSelectionModel.SelectionFlag.ClearAndSelect,
)


class ItemSelectionModel(core.ObjectMixin, core.QItemSelectionModel):
    """Keeps track of a view's selected items."""

    def __contains__(self, index: core.ModelIndex) -> bool:
        return self.isSelected(index)

    def set_current_index(self, index, flag: SelectionFlagStr):
        self.setCurrentIndex(index, SELECTION_FLAG[flag])


if __name__ == "__main__":
    model = ItemSelectionModel()
