from typing import TYPE_CHECKING, Any, ClassVar

from prettyqt import constants


if TYPE_CHECKING:
    from collections.abc import Callable

    from prettyqt import core


if TYPE_CHECKING:
    from prettyqt import core as _core

    # prettyqt item models: AbstractItemModel helpers plus data_by_index()
    class _SelectionBase(_core.AbstractItemModel):
        def data_by_index(self, index: _core.ModelIndex) -> Any: ...

else:
    _SelectionBase = object


class SelectionMixin(_SelectionBase):
    CHECKSTATE: ClassVar[dict[int, Callable]] = {}  # column: identifier

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
            self.selected[name] = value is True or value in (
                constants.CheckState.Checked,
                constants.CheckState.Checked.value,
            )
            self.dataChanged.emit(index, index)
            return True
        return super().setData(index, value, role)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        if role == constants.CHECKSTATE_ROLE and index.column() == 0:
            name = self._get_selection_id(index)
            selected = self.selected.get(name, False)
            if name not in self.selected:
                self.selected[name] = selected
            return self.to_checkstate(selected)
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
