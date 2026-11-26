from prettyqt import constants, core
from prettyqt.itemmodels.proxies.flatproxymodel import FlatProxyModel


class TableToListProxyModel(FlatProxyModel):
    """Proxy model to flatten a table to a list.

    Reshapes a table by concatenating all columns into one large column,
    so that the new rowCount equals to sourceModel rowCount * sourceModel columnCount.
    If a verticalHeader is available, it will show the original position of the cell.

    === "Without proxy"

        ```py
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        # table.proxifier.to_list()
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/tabletolistproxymodel_before.png)
        </figure>

    === "With proxy"

        ```py
        data = dict(
            first=["John", "Mary"],
            last=["Doe", "Bo"],
            height=[5.5, 6.0],
            weight=[130, 150],
        )
        model = gui.StandardItemModel.from_dict(data)
        table = widgets.TableView()
        table.set_model(model)
        table.proxifier.to_list()
        table.show()
        ```
        <figure markdown>
          ![Image title](../../images/tabletolistproxymodel_after.png)
        </figure>

    """

    ID = "table_to_list"
    ICON = "mdi6.table-pivot"

    def __init__(self, *args, header_title: str = "", **kwargs):
        self._header_title = header_title
        super().__init__(*args, **kwargs)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if self.sourceModel() is None or parent.isValid() else 1

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        source = self.sourceModel()
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self._header_title or None
            case constants.VERTICAL, constants.DISPLAY_ROLE if source is not None:
                colcount = source.columnCount()
                if colcount == 0:
                    return None
                row_section, col_section = divmod(section, colcount)
                pre = source.headerData(col_section, constants.HORIZONTAL, role)
                post = source.headerData(row_section, constants.VERTICAL, role)
                pre_str = col_section if pre is None else pre
                post_str = row_section if post is None else post
                return f"{pre_str} | {post_str}"
        return None

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if source is None or parent.isValid():
            return 0
        return source.rowCount() * source.columnCount()

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        return self.mapToSource(index).data(role) if index.isValid() else None

    def setData(
        self,
        index: core.ModelIndex,
        value,
        role: constants.ItemDataRole = constants.EDIT_ROLE,
    ) -> bool:
        source_index = self.mapToSource(index)
        if not source_index.isValid():
            return False
        return self.sourceModel().setData(source_index, value, role)

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        source_index = self.mapToSource(index)
        if not source_index.isValid():
            return super().flags(index)
        return self.sourceModel().flags(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if source is None or not proxy_idx.isValid() or source.columnCount() == 0:
            return core.ModelIndex()
        row, col = divmod(proxy_idx.row(), source.columnCount())
        return source.index(row, col)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if (
            source is None
            or not source_index.isValid()
            or source_index.parent().isValid()
        ):
            return core.ModelIndex()
        r = source_index.row() * source.columnCount() + source_index.column()
        return self.index(r, 0)

    def set_header_title(self, title: str):
        self._header_title = title
        self.headerDataChanged.emit(constants.HORIZONTAL, 0, 0)

    def get_header_title(self) -> str:
        return self._header_title

    header_title = core.Property(
        str,
        get_header_title,
        set_header_title,
        doc="Column header for resulting column",
    )


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    data = dict(
        first=["John", "Mary"],
        last=["Doe", "Bo"],
        height=[5.5, 6.0],
        weight=[130, 150],
    )
    model = gui.StandardItemModel.from_dict(data)
    table = widgets.TableView()
    table.set_model(model)
    table.show()
    table.resize(600, 500)
    table.h_header.resize_sections("stretch")
    table.set_title("Table to list")
    table.set_icon("mdi6.table-pivot")
    # table.proxifier.transpose()
    # table.proxifier.to_list()
    # splitter = debugging.ProxyComparerWidget(table.model())
    # splitter.show()
    app.exec()
