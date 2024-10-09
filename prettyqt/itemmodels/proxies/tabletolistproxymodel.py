from __future__ import annotations

from prettyqt import constants, core


class TableToListProxyModel(core.IdentityProxyModel):
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
        super().__init__(*args, **kwargs)
        self._header_title = header_title

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if self.sourceModel() is None else 1

    def headerData(
        self,
        section: int,
        orientation: constants.Orientation,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ) -> str | None:
        match orientation, role:
            case constants.HORIZONTAL, constants.DISPLAY_ROLE:
                return self._header_title or None
            case constants.VERTICAL, constants.DISPLAY_ROLE:
                col_section = section % super().columnCount()
                row_section = section // super().columnCount()
                pre = super().headerData(col_section, constants.HORIZONTAL, role)
                post = super().headerData(row_section, constants.VERTICAL, role)
                pre_str = col_section if pre is None else pre
                post_str = row_section if post is None else post
                return f"{pre_str} | {post_str}"
        return None

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        return 0 if source is None else source.rowCount() * source.columnCount()

    def index(
        self, row: int, column: int, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        source = self.sourceModel()
        if row < 0 or column < 0 or source is None:
            return core.ModelIndex()
        source_parent = self.mapToSource(parent)
        colcount = source.columnCount()
        source_index = source.index(row // colcount, row % colcount, source_parent)
        return self.mapFromSource(source_index)

    def mapToSource(self, proxy_idx: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if source is None or not proxy_idx.isValid():
            return core.ModelIndex()
        row = proxy_idx.row()
        colcount = source.columnCount()
        return source.index(row // colcount, row % colcount)

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        source = self.sourceModel()
        if source is None or not source_index.isValid():
            return core.ModelIndex()
        r = source_index.row() * source.columnCount() + source_index.column()
        return self.createIndex(r, 0, source_index.internalPointer())

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
