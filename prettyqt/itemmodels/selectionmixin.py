from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from prettyqt import constants


if TYPE_CHECKING:
    from collections.abc import Callable

    from prettyqt import core


class SelectionMixin:
    CHECKSTATE: ClassVar[dict[int, Callable]] = {}  # column: identifier
    dataChanged: core.Signal  # noqa: N815

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = {}

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if not index.isValid():
            return False
        if role == constants.CHECKSTATE_ROLE:
            name = self._get_selection_id(index)
            self.selected[name] = not self.selected[name]
            self.dataChanged.emit(index, index)
            return True
        return super().setData(index, value, role)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return False
        if role == constants.CHECKSTATE_ROLE and index.column() == 0:
            name = self._get_selection_id(index)
            selected = self.selected.get(name, False)
            if name not in self.selected:
                self.selected[name] = selected
            return selected
        return super().data(index, role)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if index.column() in self.CHECKSTATE:
            return flags | constants.IS_CHECKABLE
        return flags

    def _get_selection_id(self, index: core.ModelIndex):
        item = index.data(constants.USER_ROLE)
        if id_fn := self.CHECKSTATE.get(index.column()):
            return id_fn(item)
        return None
