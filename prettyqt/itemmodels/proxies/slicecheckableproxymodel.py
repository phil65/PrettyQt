from __future__ import annotations

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
        key = self.get_index_key(index, include_column=True)
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            return key in self._checked
        return super().data(index, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        key = self.get_index_key(index, include_column=True)
        if role == constants.CHECKSTATE_ROLE and self.indexer_contains(index):
            if is_checked := key in self._checked:
                self._checked.remove(key)
            else:
                self._checked.add(key)
            self.update_row(index.row())
            self.checkstate_changed.emit(index, not is_checked)
            return True

        return super().setData(index, role)


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
            self.set_checkstate(index, recursive=True)
        return super().setData(index, role)

    def set_checkstate(self, index: core.ModelIndex, recursive=False):
        key = self.get_index_key(index, include_column=True)
        current = self._checked.get(key)
        match current:
            case constants.CheckState.Checked:
                val = constants.CheckState.Unchecked
            case _:
                val = constants.CheckState.Checked
        self._checked[key] = val
        if recursive:
            self.set_child_states(index, val)
            self.set_parent_states(index)
        self.dataChanged.emit(index, index)
        self.checkstate_changed.emit(index, val)
        return True

    def set_parent_states(self, index: core.ModelIndex):
        indexes = []
        while (index := index.parent()).isValid():
            indexes.append(index)
        for idx in reversed(indexes):
            iterator = self.iter_tree(index)
            # next(iterator) # first one is ourself, throw it away
            states = []
            for index in iterator:
                state = index.data(constants.CHECKSTATE_ROLE)
                states.append(state)
            if all(state is True for state in states):
                val = True
            elif all(state is False for state in states):
                val = False
            else:
                val = constants.CheckState.PartiallyChecked
            key = self.get_index_key(idx, include_column=True)
            logger.debug(f"Setting {key} to {val}")
            self._checked[key] = val
            self.dataChanged.emit(idx, idx)
            self.checkstate_changed.emit(idx, val)

    def set_child_states(self, index, state):
        iterator = self.iter_tree(index)
        next(iterator)  # first one is ourself, throw it away
        for child_index in iterator:
            key = self.get_index_key(child_index, include_column=True)
            self._checked[key] = state
            self.dataChanged.emit(child_index, child_index)
            self.checkstate_changed.emit(child_index, state)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    tree = debugging.example_table()
    tree.proxifier[0, :].set_checkable()
    tree.show()
    with app.debug_mode():
        app.exec()
