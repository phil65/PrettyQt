from __future__ import annotations

from prettyqt import constants, core


class ColumnOrderProxyModel(core.IdentityProxyModel):
    """Proxy model which reorders the columns of the source model.

    Proxy model which reorders / hides the columns of the source model by passing a list
    containing the new order. Order indexes can either be an integer or the Column header.
    If not all indexes are part of the list, then the missing sections will be hidden.

    ### Example

    ```py
    table.proxifier.reorder_columns(order=[3, 2, 0])
    table.show()
    # or
    model = MyModel()
    proxy = ColumnOrderProxyModel(order=[3, 2, 0])
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "column_order"
    ICON = "mdi.reorder-vertical"

    def __init__(self, order: list[int | str], **kwargs):
        self._column_order = order
        super().__init__(**kwargs)
        self.set_column_order(order)

    def get_column_order(self) -> list[int]:
        return self._column_order

    def setSourceModel(self, model):
        super().setSourceModel(model)
        self._resolve_string_indexes()

    def _resolve_string_indexes(self):
        new_order = []
        source = self.sourceModel()
        for index in self._column_order:
            if isinstance(index, str):
                for i in range(source.columnCount()):
                    v = source.headerData(i, constants.HORIZONTAL, constants.DISPLAY_ROLE)
                    if v == index:
                        index = i
                        break
                else:
                    raise ValueError(index)
            new_order.append(index)
        self._column_order = new_order

    def set_column_order(self, order: list[int | str]):
        with self.reset_model():
            self._column_order = order
            if self.sourceModel() is not None:
                self._resolve_string_indexes()

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
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
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

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        if parent.column() > 0 or self.sourceModel() is None:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent).sibling(parent.row(), 0)
        source_index = self.sourceModel().index(
            row, self._column_order[column], source_parent
        )
        if not source_index.isValid():
            return core.ModelIndex()
        return self.createIndex(row, column, source_index.internalPointer())

    def columnCount(self, index: core.ModelIndex | None = None) -> int:
        index = index or core.ModelIndex()
        return len(self._column_order)

    def rowCount(self, index: core.ModelIndex | None = None) -> int:
        index = index or core.ModelIndex()
        if self.sourceModel() is None or index.column() > 0:
            return 0
        source_parent = self.mapToSource(index).sibling(index.row(), 0)
        return self.sourceModel().rowCount(source_parent)

    order = core.Property(
        list,
        get_column_order,
        set_column_order,
        doc="Column order",
    )


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
    model = ColumnOrderProxyModel(
        order=["b", "c"], parent=table, source_model=source_model
    )
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.exec()
