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


class ColumnJoinerProxyModel(core.IdentityProxyModel):
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

    === "Without proxy"

        ```py
        data = dict(first=["John", "Mary"], last=["Doe", "Bo"])
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        # table.proxifier.add_column(header="Full name", formatter="{1}, {0}")
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/columnjoinerproxymodel_before.png)
        </figure>

    === "With proxy"

        ```py
        data = dict(first=["John", "Mary"], last=["Doe", "Bo"])
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.add_column(header="Full name", formatter="{1}, {0}")
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/columnjoinerproxymodel_after.png)
        </figure>
    """

    ID = "column_join"
    ICON = "mdi.table-column-plus-before"

    def __init__(self, *args, **kwargs):
        self.mapping: list[ColumnMapping] = []
        super().__init__(*args, **kwargs)

    def _source_column_count(self) -> int:
        source = self.sourceModel()
        return 0 if source is None else source.columnCount()

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        if self.sourceModel() is None or parent.column() > 0:
            return 0
        return self._source_column_count() + len(self.mapping)

    def is_additional_column(self, column: int) -> bool:
        return column >= self._source_column_count()

    def _get_mapping(self, column: int) -> ColumnMapping:
        return self.mapping[column - self._source_column_count()]

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        if index.isValid() and self.is_additional_column(index.column()):
            flags = self._get_mapping(index.column()).flags
            return (
                flags
                if flags is not None
                else constants.IS_ENABLED | constants.IS_SELECTABLE
            )
        return super().flags(index)

    # Indexes of the additional columns carry the internalId of the source index of
    # the same row (like QIdentityProxyModel indexes do), so parent() still works.

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        if not self.is_additional_column(column):
            return super().index(row, column, parent)
        if not self.hasIndex(row, column, parent):
            return core.ModelIndex()
        first_col = super().index(row, 0, parent)
        return self.createIndex(row, column, first_col.internalId())

    def parent(self, *args) -> core.ModelIndex | core.QObject | None:
        if not args:  # QObject.parent()
            return core.QObject.parent(self)
        index = args[0]
        if index.isValid() and self.is_additional_column(index.column()):
            index = self.createIndex(index.row(), 0, index.internalId())
        return super().parent(index)

    def _parent_index(self, index: core.ModelIndex) -> core.ModelIndex:
        parent = self.parent(index)
        assert isinstance(parent, core.ModelIndex)
        return parent

    def sibling(self, row: int, column: int, idx: core.ModelIndex) -> core.ModelIndex:
        return self.index(row, column, self._parent_index(idx))

    def _get_text(self, index: core.ModelIndex, column: int) -> str:
        data = self.index(index.row(), column, self._parent_index(index)).data()
        return "" if data is None else str(data)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not index.isValid():
            return None
        if not self.is_additional_column(index.column()):
            return super().data(index, role)
        if role != constants.DISPLAY_ROLE:
            return None
        formatter = self._get_mapping(index.column()).formatter
        match formatter:
            case str():
                field_names = {
                    field_name
                    for _, field_name, _, _ in string.Formatter().parse(formatter)
                    if field_name
                }
                for name in field_names:
                    formatter = formatter.replace(
                        f"{{{name}}}", self._get_text(index, int(name))
                    )
                return formatter
            case Callable():
                return formatter(index)
        return None

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        if index.isValid() and self.is_additional_column(index.column()):
            return False
        return super().setData(index, value, role)

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if orientation == constants.HORIZONTAL and self.is_additional_column(section):
            if role == constants.DISPLAY_ROLE and section < self.columnCount():
                return self._get_mapping(section).header
            return None
        return super().headerData(section, orientation, role)

    def mapToSource(self, proxy_index: core.ModelIndex) -> core.ModelIndex:
        if not proxy_index.isValid() or self.is_additional_column(proxy_index.column()):
            return core.ModelIndex()
        return super().mapToSource(proxy_index)

    def add_mapping(
        self, header: str, formatter: str, flags: constants.ItemFlag | None = None
    ):
        """Add a new column to the table.

        Arguments:
            header: Label used for the section header.
            formatter: String formatter (example "{0}: {1}")
            flags: ItemFlags for new column
        """
        col = self.columnCount()
        with self.insert_columns(col, col):
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
