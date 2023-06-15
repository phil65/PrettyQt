from __future__ import annotations

import logging

from prettyqt import constants, core

logger = logging.getLogger(__name__)


class ReadOnlyProxyModel(core.IdentityProxyModel):
    ID = "read_only"

    def __init__(self, *args, columns: list[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._columns = columns

    def setData(self, index, value, role=constants.EDIT_ROLE):
        logger.warning("Trying to set data on model with read-only proxy")
        return False

    def flags(self, index):
        flags = super().flags(index)
        if self._columns is None or index.column() in self._columns:
            flags &= ~constants.IS_EDITABLE
        return flags


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    table = widgets.TableView()
    table.set_model(["a", "b", "c"])
    table.model().proxifier.get_proxy("read_only")
    table.show()
    with app.debug_mode():
        app.main_loop()
