from __future__ import annotations

from prettyqt import constants, core


class ColumnOrderProxyModel(core.IdentityProxyModel):
    ID = "column_order"

    def __init__(self, order: list[int], **kwargs):
        self._column_order = order
        super().__init__(**kwargs)

    def get_column_order(self) -> list[int]:
        return self._column_order

    def set_column_order(self, order: list[int]):
        with self.reset_model():
            self._column_order = order

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        if not proxy_index.isValid():
            return core.ModelIndex()
        return self.sourceModel().createIndex(
            proxy_index.row(),
            self._column_order[proxy_index.column()],
            proxy_index.internalPointer(),
        )

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not source_index.isValid():
            return core.ModelIndex()
        proxy_column = self._column_order.index(source_index.column())
        return self.createIndex(
            source_index.row(), proxy_column, source_index.internalPointer()
        )

    def sibling(self, row: int, column: int, index: core.ModelIndex) -> core.ModelIndex:
        if column >= len(self._column_order):
            return core.ModelIndex()
        return self.index(row, column, index.parent())

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole,
    ):
        if orientation == constants.HORIZONTAL:
            section = self._column_order[section]
        return self.sourceModel().headerData(section, orientation, role)

    def hasChildren(self, parent_index: core.ModelIndex) -> bool:
        if self.sourceModel() is None or parent_index.column() > 0:
            return False
        source_parent = self.mapToSource(parent_index).sibling(parent_index.row(), 0)
        return self.sourceModel().rowCount(source_parent) > 0

    def parent(self, index: core.ModelIndex) -> core.ModelIndex:
        source_parent = self.mapToSource(index).parent()
        if not source_parent.isValid():
            return core.ModelIndex()
        return self.createIndex(source_parent.row(), 0, source_parent.internalPointer())

    def index(self, row: int, column: int, parent_index: core.ModelIndex):
        if parent_index.column() > 0 or self.sourceModel() is None:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent_index).sibling(parent_index.row(), 0)
        source_index = self.sourceModel().index(
            row, self._column_order[column], source_parent
        )
        if not source_index.isValid():
            return core.ModelIndex()
        return self.createIndex(row, column, source_index.internalPointer())

    def columnCount(self, index: core.ModelIndex) -> int:
        return len(self._column_order)

    def rowCount(self, index: core.ModelIndex) -> int:
        if self.sourceModel() is None or index.column() > 0:
            return 0
        source_parent = self.mapToSource(index).sibling(index.row(), 0)
        return self.sourceModel().rowCount(source_parent)

    column_order = core.Property(list, get_column_order, set_column_order)


if __name__ == "__main__":
    from prettyqt import gui, widgets

    data = dict(
        a=["abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedf", "abcdedfaa"],
        b=[10000000, 2, 3, 4, 5, 6],
        c=[1, 2, 3, 4, 5, 6],
        d=[100000000, 2, 3, 4, 5, 6],
        e=[1000000, 2, 3, 4, 5, 6],
    )
    source_model = gui.StandardItemModel.from_dict(data)
    app = widgets.app()
    table = widgets.TableView()
    model = ColumnOrderProxyModel([1, 2], parent=table)
    model.setSourceModel(source_model)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
