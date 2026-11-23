from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, core


if TYPE_CHECKING:
    from collections.abc import Sequence


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

    def __init__(self, order: Sequence[int | str], **kwargs):
        self._column_order = list(order)
        super().__init__(**kwargs)
        self.set_column_order(self._column_order)

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

    # Proxy indexes carry the internalId of the corresponding source index
    # (like QIdentityProxyModel does), so the C++ implementation of
    # QIdentityProxyModel.mapToSource can be used to build the source index.
    # (Never use internalPointer() here, source indexes may come from C++ models.)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        if not proxy_index.isValid() or self.sourceModel() is None:
            return core.ModelIndex()
        if proxy_index.column() >= len(self._column_order):
            return core.ModelIndex()
        source_column = self._column_order[proxy_index.column()]
        helper = self.createIndex(
            proxy_index.row(), source_column, proxy_index.internalId()
        )
        return super().mapToSource(helper)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not source_index.isValid() or source_index.column() not in self._column_order:
            return core.ModelIndex()
        proxy_column = self._column_order.index(source_index.column())
        return self.createIndex(
            source_index.row(), proxy_column, source_index.internalId()
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
        if self.sourceModel() is None:
            return None
        if orientation == constants.HORIZONTAL:
            if not 0 <= section < len(self._column_order):
                return None
            section = self._column_order[section]
        return self.sourceModel().headerData(section, orientation, role)

    def _source_parent(self, parent: core.ModelIndex) -> core.ModelIndex:
        """Source index of the first column of given proxy parent."""
        if not parent.isValid():
            return core.ModelIndex()
        return self.mapToSource(parent).siblingAtColumn(0)

    def hasChildren(self, parent: core.ModelIndex | None = None) -> bool:
        parent = parent or core.ModelIndex()
        if self.sourceModel() is None or parent.column() > 0:
            return False
        return self.sourceModel().hasChildren(self._source_parent(parent))

    def parent(self, *args) -> core.ModelIndex | core.QObject | None:
        if not args:  # QObject.parent()
            return core.QObject.parent(self)
        index = args[0]
        if not index.isValid():
            return core.ModelIndex()
        source_parent = self.mapToSource(index).parent()
        if not source_parent.isValid():
            return core.ModelIndex()
        return self.createIndex(source_parent.row(), 0, source_parent.internalId())

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        if parent.column() > 0 or self.sourceModel() is None:
            return core.ModelIndex()
        if not 0 <= column < len(self._column_order):
            return core.ModelIndex()
        source_index = self.sourceModel().index(
            row, self._column_order[column], self._source_parent(parent)
        )
        if not source_index.isValid():
            return core.ModelIndex()
        return self.createIndex(row, column, source_index.internalId())

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        if self.sourceModel() is None or parent.column() > 0:
            return 0
        return len(self._column_order)

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        if self.sourceModel() is None or parent.column() > 0:
            return 0
        return self.sourceModel().rowCount(self._source_parent(parent))

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
