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
    flags: constants.ItemFlag | None = None


class ColumnJoinerProxyModel(core.AbstractProxyModel):
    """Proxy model which joins the contents of several columns.

    The columns are joined based on a formatter and appended to the end of the model
    as a new column.

    The formatter must look like `{0} - {1}: {4}`.
    The format codes are then populated with the content of given columns,
    in this case it would be `{Text of column 0} - {Text of Column 1}: {Text of Column 4}`

    ### Example

    ```py
    table.proxifier.join_columns(formatter="{0} - {2}", header="New column")
    table.show()
    # or
    model = MyModel()
    proxy = ColumnJoinerProxyModel()
    proxy.set_source_model(model)
    proxy.add_column(formatter="{0} - {2}", header="New column")
    proxy.add_column(formatter="{4}: {5}", header="Another column")
    table.set_model(proxy)
    table.show()
    ```
    """

    ID = "column_join"
    ICON = "mdi.table-column-plus-before"

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

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        return self.sourceModel().rowCount()

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        column = index.column()
        if self.is_additional_column(column):
            flags = self.mapping[column - self.columnCount()].flags
            return (
                flags
                if flags is not None
                else constants.IS_ENABLED | constants.IS_SELECTABLE
            )
        return self.sourceModel().flags(index)

    def is_additional_column(self, column: int):
        col_count = self.sourceModel().columnCount()
        return column >= col_count

    def index(self, row, column, parent):
        if self.is_additional_column(column):
            return self.createIndex(row, column, core.ModelIndex())
        return self.sourceModel().index(row, column, parent)

    def parent(self, index=None):
        if index is None:
            return super().parent()
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
                            idx = self.index(index.row(), int(name), index.parent())
                            data = self.data(idx)
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
        return self.sourceModel().index(proxy_index.row(), column, proxy_index.parent())

    def mapFromSource(self, index):
        if self.is_additional_column(index.column()):
            return core.ModelIndex()
        return self.sourceModel().index(index.row(), index.column(), index.parent())

    def add_mapping(
        self, header: str, formatter: str, flags: constants.ItemFlag | None = None
    ):
        """Add a new column to the table.

        Arguments:
            header: Label used for the section header.
            formatter: String formatter (example "{0}: {1}")
            flags: ItemFlags for new column
        """
        self.mapping.append(ColumnMapping(formatter, header, flags))


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    data = dict(first=["John", "Mary"], last=["Doe", "Bo"])
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.proxifier.add_column(header="Full name", formatter="{1}, {0}")
    table.show()
    table.resize(400, 130)
    table.h_header.resize_sections("stretch")
    table.set_title("ColumnJoinerProxymodel")
    table.set_icon("mdi.table-column-plus-before")
    with app.debug_mode():
        app.exec()
