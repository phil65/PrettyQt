from __future__ import annotations

import logging
from typing import Any

from prettyqt import constants, core
from prettyqt.utils import helpers


logger = logging.getLogger(__name__)


class ReadOnlyProxyModel(core.IdentityProxyModel):
    ID = "read_only"

    def __init__(self, *args, index=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._index = index or (slice(None), slice(None))

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        read_only = helpers.is_position_in_index(index.column(), index.row(), self._index)
        if read_only:
            logger.warning("Trying to set data on region covered by read-only proxy")
            return False
        return super().data(index, value, role)

    def flags(self, index):
        flags = super().flags(index)
        read_only = helpers.is_position_in_index(index.column(), index.row(), self._index)
        if read_only:
            flags &= ~constants.IS_EDITABLE
        return flags


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    table = widgets.TableView()
    table.set_model(["a", "b", "c"])
    table.proxifier.get_proxy("read_only", index=(0, 0))
    table.show()
    with app.debug_mode():
        app.main_loop()
