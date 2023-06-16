from __future__ import annotations

from collections.abc import Callable
import dataclasses
import logging
import string

from prettyqt import constants, core

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ColumnMapping:
    formatter: str | Callable
    header: str


class ColumnJoinerProxyModel(core.IdentityProxyModel):
    ID = "column_join"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapping = list()

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return (
            0
            if self.sourceModel() is None
            else self.sourceModel().columnCount(parent) + len(self.mapping)
        )

    def is_additional_column(self, column: int):
        col_count = self.sourceModel().columnCount()
        return col_count <= column <= col_count + len(self.mapping)

    def index(self, row, column, parent):
        extra_col = self.sourceModel().columnCount(parent) - column
        if extra_col >= 0:
            pointer = super().index(row, 0, parent).internalPointer()
            return self.createIndex(row, column, pointer)
        return super().index(row, column, parent)

    def parent(self, child=None):
        if child is None:
            return super().parent()
        extra_col = self.sourceModel().columnCount() - child.column()
        if extra_col >= 0:
            proxy_sibling = self.createIndex(child.row(), 0, child.internalPointer())
            return super().parent(proxy_sibling)
        return super().parent(child)

    def flags(self, index):
        extra_col = self.sourceModel().columnCount() - index.column()
        if extra_col >= 0:
            return constants.IS_SELECTABLE | constants.IS_ENABLED
        return self.sourceModel().flags(self.mapToSource(index))

    def data(self, index, role=constants.DISPLAY_ROLE):
        col_count = self.sourceModel().columnCount()
        column = index.column()
        if self.is_additional_column(column):
            if role == constants.DISPLAY_ROLE:
                mapper = self.mapping[column - col_count]
                field_names = [v[1] for v in string.Formatter().parse(mapper.formatter)]
                formatter = mapper.formatter
                match formatter:
                    case str():
                        for name in field_names:
                            data = self.data(
                                self.index(index.row(), int(name), index.parent())
                            )
                            formatter = formatter.replace(f"{{{name}}}", data)
                        return formatter
                    case Callable():
                        return formatter(index)
            return None
        return super().data(index, role)

    def headerData(self, section, orientation, role=None):
        if orientation == constants.HORIZONTAL:
            if self.is_additional_column(section):
                if role == constants.DISPLAY_ROLE:
                    mapper = self.mapping[section - section]
                    return mapper.header
                return None
        return super().headerData(section, orientation, role)

    def mapToSource(self, proxy_index):
        if not proxy_index.isValid():
            return core.ModelIndex()
        column = proxy_index.column()
        if column >= self.sourceModel().columnCount():
            return core.ModelIndex()
        return super().mapToSource(proxy_index)

    # def mapFromSource(self, index):
    #     return self.index(index.row(), index.column(), index.parent())

    def mapSelectionToSource(self, selection):
        source_selection = core.ItemSelection()
        if self.sourceModel() is None:
            return source_selection
        source_col_count = self.sourceModel().columnCount()
        for item in selection:
            top_left = item.topLeft()
            bottom_right = item.bottomRight()
            if bottom_right.column() >= source_col_count:
                bottom_right = bottom_right.sibling(
                    bottom_right.row(), source_col_count - 1
                )
            irange = core.ItemSelectionRange(
                self.mapToSource(top_left), self.mapToSource(bottom_right)
            )
            iselection = core.ItemSelection()
            iselection << irange
            source_selection.merge(iselection, core.ItemSelection.SelectionFlag.Select)
        return source_selection

    def buddy(self, proxy_index):
        column = proxy_index.column()
        if column >= self.sourceModel().columnCount():
            return proxy_index
        return super().buddy(proxy_index)

    def sibling(self, row, column, index):
        if row == index.row() and column == index.column():
            return index
        return self.index(row, column, self.parent(index))

    def add_mapping(self, column_name: str, formatter: str):
        """Form: for example "{0} ({1}), with numbers referencing the columns."""
        self.mapping.append(ColumnMapping(formatter, column_name))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    # tree = debugging.example_tree()
    class Model(core.AbstractTableModel):
        def rowCount(self, index=None):
            return 50

        def columnCount(self, index=None):
            return 50

        def data(self, index, role=None):
            match role, index.column():
                case constants.DISPLAY_ROLE | constants.USER_ROLE, _:
                    return "test"

        def flags(self, index):
            return (
                super().flags(index)
                | constants.IS_EDITABLE
                | constants.IS_ENABLED
                | constants.IS_SELECTABLE
            )

    model = Model()
    table = widgets.TableView()
    proxy = ColumnJoinerProxyModel()
    proxy.setSourceModel(model)
    proxy.add_mapping(column_name="header", formatter="{0} {1}")
    table.set_model(proxy)
    table.show()
    table.resize(1000, 1000)
    with app.debug_mode():
        app.main_loop()
