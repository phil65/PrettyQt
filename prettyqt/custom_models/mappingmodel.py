from __future__ import annotations

from prettyqt import constants, core, custom_models


class MappingModel(custom_models.ListMixin, core.AbstractTableModel):
    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case (dict(), *_):
                return True
            case _:
                return False

    def columnCount(self, index: core.ModelIndex | None = None):
        return len(self.items[0]) if self.items else 0

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return list(self.items[0].keys())[section]

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        item = self.data_by_index(index)
        match role:
            case constants.DISPLAY_ROLE:
                key = self.headerData(index.column(), constants.HORIZONTAL)
                return item[key]


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
