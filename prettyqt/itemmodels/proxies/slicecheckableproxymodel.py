import logging
from typing import Any

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


class SliceCheckableProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to make a model checkable.

    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[::2, 2:].modify(xyz)
    table.show()
    # or
    indexer = (slice(None, None, 2), slice(2, None))
    proxy = itemmodels.SliceCheckableProxyModel(indexer=indexer)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "checkable"
    checkstate_changed = core.Signal(core.ModelIndex, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checked: set[tuple[int, int]] = set()

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        if not index.isValid():
            return super().flags(index)
        if self.indexer_contains(index):
            return super().flags(index) | constants.IS_CHECKABLE
        return super().flags(index)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            key = self.get_index_key(index, include_column=True)
            return self.to_checkstate(key in self._checked)
        return super().data(index, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            key = self.get_index_key(index, include_column=True)
            checked = self.from_checkstate(value)
            if checked == (key in self._checked):
                return True
            if checked:
                self._checked.add(key)
            else:
                self._checked.discard(key)
            self.dataChanged.emit(index, index, [constants.CHECKSTATE_ROLE])
            self.checkstate_changed.emit(index, checked)
            return True
        return super().setData(index, value, role)


class SliceCheckableTreeProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to make a tree model checkable.

    In contrast to SliceCheckableProxyModel, any checkstate change is propagated to
    parent and child indexes. (child indexes will also get the new checkstate, parent
    indexes will become partially checked if needed.)

    ### Example

    ```py
    model = MyModel()
    table = widgets.TreeView()
    table.set_model(model)
    table.proxifier[:, 0].set_checkable(tree=True)
    table.show()
    # or
    proxy = itemmodels.SliceCheckableTreeProxyModel(indexer=0)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "checkable_tree"
    checkstate_changed = core.Signal(core.ModelIndex, constants.CheckState)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checked: dict[tuple[int, int], constants.CheckState] = {}

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        if not index.isValid():
            return super().flags(index)
        if self.indexer_contains(index):
            # TODO: do i need to mess with ItemDataFlag.ItemIsTristate?
            return super().flags(index) | constants.IS_CHECKABLE
        return super().flags(index)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            key = self.get_index_key(index, include_column=True)
            return self._checked.get(key, constants.CheckState.Unchecked)
        return super().data(index, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            state = (
                constants.CheckState.Checked
                if self.from_checkstate(value)
                else constants.CheckState.Unchecked
            )
            self.set_checkstate(index, state, recursive=True)
            return True
        return super().setData(index, value, role)

    def _set_state(self, index: core.ModelIndex, state: constants.CheckState):
        key = self.get_index_key(index, include_column=True)
        if self._checked.get(key, constants.CheckState.Unchecked) == state:
            return
        self._checked[key] = state
        self.dataChanged.emit(index, index, [constants.CHECKSTATE_ROLE])
        self.checkstate_changed.emit(index, state)

    def set_checkstate(
        self,
        index: core.ModelIndex,
        state: constants.CheckState | None = None,
        recursive: bool = False,
    ):
        """Set the checkstate of given index (toggle if state is None).

        If recursive is True, children get the same state and the parents are
        updated (partially checked if needed).
        """
        if state is None:
            key = self.get_index_key(index, include_column=True)
            current = self._checked.get(key, constants.CheckState.Unchecked)
            state = (
                constants.CheckState.Unchecked
                if current == constants.CheckState.Checked
                else constants.CheckState.Checked
            )
        self._set_state(index, state)
        if recursive:
            self.set_child_states(index, state)
            self.set_parent_states(index)
        return True

    def set_parent_states(self, index: core.ModelIndex):
        """Update checkstate of all ancestors based on their direct children."""
        column = index.column()
        parent = index.parent()
        while parent.isValid():
            parent = parent.sibling(parent.row(), column)
            children = [
                self.index(row, column, parent) for row in range(self.rowCount(parent))
            ]
            states = {self.data(child, constants.CHECKSTATE_ROLE) for child in children}
            if states == {constants.CheckState.Checked}:
                val = constants.CheckState.Checked
            elif states <= {constants.CheckState.Unchecked, None}:
                val = constants.CheckState.Unchecked
            else:
                val = constants.CheckState.PartiallyChecked
            self._set_state(parent, val)
            parent = parent.parent()

    def set_child_states(self, index: core.ModelIndex, state: constants.CheckState):
        """Set checkstate of all (already fetched) descendants."""
        column = index.column()
        for row in range(self.rowCount(index.siblingAtColumn(0))):
            child = self.index(row, column, index.siblingAtColumn(0))
            self._set_state(child, state)
            self.set_child_states(child, state)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    tree = debugging.example_table()
    tree.proxifier[0, :].set_checkable()
    tree.show()
    with app.debug_mode():
        app.exec()
