from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core

logger = logging.getLogger(__name__)


class CheckableProxyModel(core.IdentityProxyModel):
    ID = "checkable"
    checkstate_changed = core.Signal(core.ModelIndex, bool)  # row, state

    def __init__(self, column: int = 0, **kwargs):
        super().__init__(**kwargs)
        self._column = column
        self._checked: set[int] = set()

    def flags(self, index):
        if not index.isValid():
            return super().flags(index)
        if index.column() == self._column:
            return super().flags(index) | constants.IS_CHECKABLE
        return super().flags(index)

    def data(self, index, role=constants.DISPLAY_ROLE):
        if role == constants.CHECKSTATE_ROLE and index.column() == self._column:
            return index.row() in self._checked

        return super().data(index, role)

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if role == constants.CHECKSTATE_ROLE and index.column() == self._column:
            if index.row() in self._checked:
                self._checked.remove(index.row())
                self.update_row(index.row())
                self.checkstate_changed.emit(index, False)
                return True
            elif index.row() not in self._checked:
                self._checked.add(index.row())
                self.update_row(index.row())
                self.checkstate_changed.emit(index, True)
                return True

        return super().setData(index, role)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    tree = debugging.example_tree()
    tree.proxifier.get_proxy("checkable")
    tree.show()
    with app.debug_mode():
        app.main_loop()
