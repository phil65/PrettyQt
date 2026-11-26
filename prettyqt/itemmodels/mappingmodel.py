from collections.abc import Mapping, Sequence

from prettyqt import constants, core, itemmodels


class MappingModel(itemmodels.ListMixin, core.AbstractTableModel):
    """Table model for a list of mappings. Columns are the keys of the first mapping."""

    SUPPORTS = Sequence[Mapping]

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (Mapping(), *_):
                return True
            case _:
                return False

    def _keys(self) -> list:
        return list(self.items[0].keys()) if self.items else []

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._keys())

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                keys = self._keys()
                return str(keys[section]) if 0 <= section < len(keys) else None
        return None

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        item = self.data_by_index(index)
        key = self._keys()[index.column()]
        value = item.get(key)
        match role:
            case constants.DISPLAY_ROLE if not isinstance(value, bool):
                return "" if value is None else str(value)
            case constants.CHECKSTATE_ROLE if isinstance(value, bool):
                return self.to_checkstate(value)
            case constants.EDIT_ROLE | constants.USER_ROLE:
                return value
        return None


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    dct = dict(a=2, b="hallo", c="hall")
    dct2 = dict(a=2, b="hallo2", c="hallo3")
    model = MappingModel(items=[dct, dct2])
    table = widgets.TableView()
    table.set_model(model)
    table.show()
    app.exec()
