from __future__ import annotations

import logging

from prettyqt import custom_models, constants, core


logger = logging.getLogger(__name__)


class SliceChangeFlagsProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "change_flags"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._flags_to_remove: constants.ItemFlag = constants.ItemFlag(0)
        self._flags_to_add: constants.ItemFlag = constants.ItemFlag(0)

    # def setData(
    #     self,
    #     index: core.ModelIndex,
    #     value: Any,
    #     role: constants.ItemDataRole = constants.EDIT_ROLE,
    # ) -> bool:
    #     if self.indexer.contains(index):
    #         logger.warning("Trying to set data on region covered by read-only proxy")
    #         return False
    #     return super().setData(index, value, role)

    def flags(self, index):
        flags = super().flags(index)
        if self.indexer_contains(index):
            for flag in self._flags_to_remove:
                flags &= ~flag
            for flag in self._flags_to_add:
                flags |= flag
        return flags

    def set_flags_to_add(self, flags: constants.ItemFlag):
        self._flags_to_add = flags

    def get_flags_to_add(self) -> constants.ItemFlag:
        return self._flags_to_add

    def set_flags_to_remove(self, flags: constants.ItemFlag):
        self._flags_to_remove = flags

    def get_flags_to_remove(self) -> constants.ItemFlag:
        return self._flags_to_remove

    flags_to_add = core.Property(constants.ItemFlag, get_flags_to_add, set_flags_to_add)
    flags_to_remove = core.Property(
        constants.ItemFlag, get_flags_to_remove, set_flags_to_remove
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    table = widgets.TableView()
    table.set_model_for(["a", "b", "c"])
    proxy = table.proxifier.get_proxy("change_flags", indexer=(0, 0))
    proxy._flags_to_remove = constants.IS_EDITABLE
    table.show()
    with app.debug_mode():
        app.main_loop()
