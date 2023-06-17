from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core, custom_models

logger = logging.getLogger(__name__)


class CheckableProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "checkable"
    checkstate_changed = core.Signal(core.ModelIndex, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checked: set[tuple[int, int]] = set()

    def flags(self, index):
        if not index.isValid():
            return super().flags(index)
        if self.indexer_contains(index):
            return super().flags(index) | constants.IS_CHECKABLE
        return super().flags(index)

    def data(self, index: core.ModelIndex, role=constants.DISPLAY_ROLE):
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


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    tree = debugging.example_table()
    tree.proxifier[::2, 1::2].set_checkable()
    tree.show()
    with app.debug_mode():
        app.main_loop()
