from __future__ import annotations

import logging

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


class SliceChangeFlagsProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to selectively change the ItemFlags of the source model.

    === "Without proxy"

        ```py
        table = widgets.TreeView()
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        source_model = gui.StandardItemModel.from_dict(data)
        table.set_model(source_model)
        # table.proxifier.change_flags(enabled=False)
        ```
        <figure markdown>
          ![Image title](../../images/slicechangeflagsproxymodel_before.png)
        </figure>

    === "With proxy"

        ```py
        table = widgets.TreeView()
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        source_model = gui.StandardItemModel.from_dict(data)
        table.set_model(source_model)
        table.proxifier.change_flags(enabled=False)
        ```
        <figure markdown>
          ![Image title](../../images/slicechangeflagsproxymodel_after.png)
        </figure>


    Supports changing all ItemRoles by passing keyword arguments.

    Possible keyword arguments:

    * `selectable`: ItemFlag.ItemIsSelectable,
    * `editable`: ItemFlag.ItemIsEditable,
    * `drag_enabled`: ItemFlag.ItemIsDragEnabled,
    * `drop_enabled`: ItemFlag.ItemIsDropEnabled,
    * `user_checkable`: ItemFlag.ItemIsUserCheckable,
    * `enabled`: ItemFlag.ItemIsEnabled,
    * `auto_tristate`: ItemFlag.ItemIsAutoTristate,
    * `never_has_children`: ItemFlag.ItemNeverHasChildren,
    * `user_tristate`: ItemFlag.ItemIsUserTristate,



    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier[::2, 2:].change_flags(readable=False)
    table.show()
    ```

    or

    ```py
    indexer = (slice(None, None, 2), slice(2, None))
    proxy = itemmodels.SliceChangeFlagsProxyModel(indexer=indexer, readable=False)
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "change_flags"
    ICON = "mdi.flag"

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

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        if self.indexer_contains(index):
            for flag in self._flags_to_remove:
                flags &= ~flag
            for flag in self._flags_to_add:
                flags |= flag
        return flags

    def set_flags_to_add(self, flags: constants.ItemFlag):
        with self.change_layout():
            self._flags_to_add = flags

    def get_flags_to_add(self) -> constants.ItemFlag:
        return self._flags_to_add

    def set_flags_to_remove(self, flags: constants.ItemFlag):
        with self.change_layout():
            self._flags_to_remove = flags

    def get_flags_to_remove(self) -> constants.ItemFlag:
        return self._flags_to_remove

    flags_to_add = core.Property(
        constants.ItemFlag,
        get_flags_to_add,
        set_flags_to_add,
        doc="Flags to set",
    )
    flags_to_remove = core.Property(
        constants.ItemFlag,
        get_flags_to_remove,
        set_flags_to_remove,
        doc="Flags to unset",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    data = dict(
        first=["John", "Mary"],
        last=["Doe", "Bo"],
        height=[5.5, 6.0],
        weight=[130, 150],
    )
    model = gui.StandardItemModel.from_dict(data)
    app = widgets.app()
    table = widgets.TableView()
    table.set_model(model)
    # proxy = table.proxifier[:, 2:].change_flags(enabled=False)
    table.show()
    table.resize(600, 150)
    table.h_header.resize_sections("stretch")
    table.set_title("Change flags")
    table.set_icon("mdi.flag")
    with app.debug_mode():
        app.exec()
