from __future__ import annotations

from collections.abc import Callable, Mapping

from bidict import bidict

from prettyqt import constants, core, itemmodels


class SliceMapRoleProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model for mapping one role to another.

    Mapping can be changed by passing a dictionary with source role as key and target_role
    as value.
    Py passing an optional converter function, values which are mapped can be modified.

    ### Example

    ```py
    source_model = FsSpecTreemodel("file")
    table = widgets.TableView()
    mapping = {source_model.Roles.ProtocolPathRole: constants.DISPLAY_ROLE}
    model = SliceMapRoleProxyModel(mapping, indexer=0, parent=table)
    model.setSourceModel(source_model)
    table.set_model(model)
    table.show()
    # or
    table.proxifier.map_role(source_model.Roles.ProtocolPathRole, constants.DISPLAY_ROLE)
    ```
    """

    ID = "map_role"
    ICON = "mdi.directions-fork"

    def __init__(
        self,
        mapping: Mapping[constants.ItemDataRole, constants.ItemDataRole],
        converter: Callable | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._mapping = bidict(mapping)
        self._converter = converter

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role in self._mapping.inverse and self.indexer_contains(index):
            value = super().data(index, self._mapping.inverse[role])
            return self._converter(value) if self._converter else value
        return super().data(index, role)

    def set_mapping(
        self,
        mapping: Mapping[constants.ItemDataRole, constants.ItemDataRole],
    ):
        with self.reset_model():
            self._mapping = bidict(mapping)

    def get_mapping(self) -> Mapping[constants.ItemDataRole, constants.ItemDataRole]:
        return self._mapping

    mapping = core.Property(
        dict,
        get_mapping,
        set_mapping,
        doc="Mapping of ItemRoles",
    )


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.itemmodels import fsspecmodel

    source_model = fsspecmodel.FSSpecTreeModel("file")
    app = widgets.app()
    table = widgets.TableView()
    mapping = {
        source_model.Roles.ProtocolPathRole: constants.DISPLAY_ROLE,
    }
    model = SliceMapRoleProxyModel(mapping, indexer=0, parent=table)
    model.setSourceModel(source_model)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
