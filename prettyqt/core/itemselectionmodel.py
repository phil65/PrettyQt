from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
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

SELECTION_FLAG: bidict[
    SelectionFlagStr, QtCore.QItemSelectionModel.SelectionFlag
] = bidict(
    none=QtCore.QItemSelectionModel.SelectionFlag.NoUpdate,
    clear=QtCore.QItemSelectionModel.SelectionFlag.Clear,
    select=QtCore.QItemSelectionModel.SelectionFlag.Select,
    deselect=QtCore.QItemSelectionModel.SelectionFlag.Deselect,
    toggle=QtCore.QItemSelectionModel.SelectionFlag.Toggle,
    current=QtCore.QItemSelectionModel.SelectionFlag.Current,
    rows=QtCore.QItemSelectionModel.SelectionFlag.Rows,
    columns=QtCore.QItemSelectionModel.SelectionFlag.Columns,
    select_current=QtCore.QItemSelectionModel.SelectionFlag.SelectCurrent,
    toggle_current=QtCore.QItemSelectionModel.SelectionFlag.ToggleCurrent,
    clear_and_select=QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect,
)


class ItemSelectionModel(core.ObjectMixin, QtCore.QItemSelectionModel):
    def set_current_index(self, index, flag: SelectionFlagStr):
        self.setCurrentIndex(index, SELECTION_FLAG[flag])
