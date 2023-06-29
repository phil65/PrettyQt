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
    flags: constants.ItemFlag = constants.IS_ENABLED | constants.IS_SELECTABLE


class ColumnJoinerProxyModel(core.AbstractProxyModel):
    ID = "column_join"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapping = []

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return (
            0
            if self.sourceModel() is None
            else self.sourceModel().columnCount(parent) + len(self.mapping)
        )

    def rowCount(self, parent: core.ModelIndex | None = None):
        return self.sourceModel().rowCount()

    def flags(self, index: core.ModelIndex):
        column = index.column()
        if self.is_additional_column(column):
            return self.mapping[column - self.columnCount()].flags
        return self.sourceModel().flags(index)

    def is_additional_column(self, column: int):
        col_count = self.sourceModel().columnCount()
        return column >= col_count

    def index(self, row, column, parent):
        if self.is_additional_column(column):
            return self.createIndex(row, column, core.ModelIndex())
        return self.sourceModel().index(row, column, parent)

    def parent(self, index=None):
        if self.is_additional_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().parent(index)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
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

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if orientation == constants.HORIZONTAL and self.is_additional_column(section):
            if role == constants.DISPLAY_ROLE:
                mapper = self.mapping[section - self.columnCount()]
                return mapper.header
            return None
        return super().headerData(section, orientation, role)

    def mapToSource(self, proxy_index):
        if not proxy_index.isValid():
            return core.ModelIndex()
        column = proxy_index.column()
        if self.is_additional_column(column):
            return core.ModelIndex()
        return self.sourceModel().index(
            proxy_index.row(), proxy_index.column(), proxy_index.parent()
        )

    def mapFromSource(self, index):
        if self.is_additional_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().index(index.row(), index.column(), index.parent())

    def add_mapping(self, column_name: str, formatter: str):
        """Form: for example "{0} ({1}), with numbers referencing the columns."""
        self.mapping.append(ColumnMapping(formatter, column_name))


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    dct = dict(a=[1, 2, 3], b=["d", "e", "f"], c=["te", "st", "test"], d=["x", "y", "z"])
    model = gui.StandardItemModel.from_dict(dct)
    table = widgets.TableView()
    proxy = ColumnJoinerProxyModel()
    proxy.setSourceModel(model)
    proxy.add_mapping(column_name="header", formatter="{0} {1}")
    proxy.add_mapping(column_name="header2", formatter="{2} {3}")
    table.set_model(proxy)
    table.show()
    table.resize(1000, 1000)
    with app.debug_mode():
        app.exec()
