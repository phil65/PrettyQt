from __future__ import annotations

from prettyqt import constants, core


class FlattenTreeProxyModel(core.AbstractProxyModel):
    ID = "flatten_tree"

    def __init__(self, parent: widgets.QWidget | None = None, **kwargs):
        self._leaves_only = False
        self._show_path = False
        self._source_column = 0
        self.PATH_SEPARATOR = " / "
        self._source_root_index = core.ModelIndex()
        self._source_key: list[tuple[int, ...]] = []
        self._source_offset: dict[tuple[int, ...], int] = {}
        super().__init__(parent, **kwargs)

    def setSourceModel(self, model: core.QAbstractItemModel):
        if (old_model := self.sourceModel()) is not None:
            old_model.dataChanged.disconnect(self._source_data_changed)
            old_model.rowsInserted.disconnect(self._on_reset)
            old_model.rowsRemoved.disconnect(self._on_reset)
            old_model.rowsMoved.disconnect(self._on_row_move)
        with self.reset_model():
            super().setSourceModel(model)
            self._update_mapping()

        model.dataChanged.connect(self._source_data_changed)
        model.rowsInserted.connect(self._on_reset)
        model.rowsRemoved.connect(self._on_reset)
        model.rowsMoved.connect(self._on_row_move)

    def set_source_column(self, column: int):
        with self.reset_model():
            self._source_column = column
            self._update_mapping()

    def get_source_column(self) -> int:
        return self._source_column

    def set_root_index(self, root_index: core.ModelIndex):
        with self.reset_model():
            self._source_root_index = root_index
            self._update_mapping()

    def get_root_index(self) -> core.ModelIndex:
        return self._source_root_index

    def set_leaves_only(self, leaves_only: bool):
        if leaves_only != self._leaves_only:
            with self.reset_model():
                self._leaves_only = leaves_only
                self._update_mapping()

    def is_leaves_only(self) -> bool:
        return self._leaves_only

    def set_show_path(self, show: bool):
        if show != self._show_path:
            with self.reset_model():
                self._show_path = show

    def is_path_shown(self) -> bool:
        return self._show_path

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not source_index.isValid():
            return source_index
        key = self.get_index_key(source_index)
        row = self._source_offset[key] + source_index.row()
        return self.index(row, 0)

    def mapToSource(self, index: core.ModelIndex) -> core.ModelIndex:
        if not index.isValid():
            return index
        row = index.row()
        source_key_path = self._source_key[row]
        return self.source_index_from_key(source_key_path)

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        return (
            core.ModelIndex()
            if parent.isValid()
            else self.createIndex(row, column, row)  # object=row)
        )

    def parent(self, child=None) -> core.ModelIndex:
        return super().parent() if child is None else core.ModelIndex()

    def rowCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._source_key)

    def columnCount(self, parent: core.ModelIndex | None = None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else 1

    def flags(self, index: core.ModelIndex) -> constants.ItemFlag:
        flags = super().flags(index)
        return flags
        # this would disable non-leave items
        # index = self.mapToSource(index)
        # model = self.sourceModel()
        # enabled = flags & constants.ItemFlag.ItemIsEnabled
        # if model is not None and model.rowCount(index) > 0 and enabled:
        #     flags ^= constants.ItemFlag.ItemIsEnabled
        # return flags

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.DISPLAY_ROLE and self._show_path:
            index = self.mapToSource(index)
            model = self.sourceModel()
            path = model.get_breadcrumbs_path(index)
            return self.PATH_SEPARATOR.join(str(i) for i in path)
        return super().data(index, role)

    def _update_mapping(self):
        if self.sourceModel() is None:
            return
        self._source_key, self._source_offset = self.get_source_mapping(self._leaves_only)

    def _source_data_changed(self, top: core.ModelIndex, bottom: core.ModelIndex):
        changed_indexes = [top.sibling(i, 0) for i in range(top.row(), bottom.row() + 1)]
        for ind in changed_indexes:
            self.dataChanged.emit(ind, ind)

    def _on_reset(self, parent: core.ModelIndex, start: int, end: int):
        with self.reset_model():
            self._update_mapping()

    def _on_row_move(
        self, source_parent, source_start, source_end, dest_parent, dest_row
    ):
        with self.reset_model():
            self._update_mapping()

    leaves_only = core.Property(
        bool,
        is_leaves_only,
        set_leaves_only,
        doc="Whether to only show the tree leaves",
    )
    show_path = core.Property(
        bool,
        is_path_shown,
        set_show_path,
        doc="Show the complete path in first column",
    )


if __name__ == "__main__":
    from prettyqt import itemmodels, widgets

    app = widgets.app()
    table = widgets.TreeView()
    source_model = itemmodels.ParentClassTreeModel(widgets.Frame)
    table.set_model(source_model)
    table.expandAll()
    table.proxifier.flatten(leaves_only=True)
    table.show()
    table.resize(600, 500)
    table.h_header.resize_sections("stretch")
    table.set_icon("mdi6.table-pivot")
    table.set_title("Flatten")
    app.exec()
