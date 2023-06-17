from __future__ import annotations

import logging
from typing import Any

from prettyqt import custom_models, constants, core


logger = logging.getLogger(__name__)


class ReadOnlyProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "read_only"

    def setData(
        self,
        index: core.ModelIndex,
        value: Any,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if self.indexer.contains(index):
            logger.warning("Trying to set data on region covered by read-only proxy")
            return False
        return super().setData(index, value, role)

    def flags(self, index):
        flags = super().flags(index)
        if self.indexer_contains(index):
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
