from __future__ import annotations

import enum

from prettyqt import constants, core
from prettyqt.qt import QtCore


class FlatteningMode(enum.IntEnum):
    """Flattening modes."""

    Default = 1
    InternalNodesDisabled = 2
    LeavesOnly = 4


class DisplayMode(enum.IntEnum):
    """Display modes."""

    Path = 1
    Title = 2


class FlattenedTreeProxyModel(core.AbstractProxyModel):
    ID = "flatten_tree"

    FlatteningMode = FlatteningMode
    core.Enum(FlatteningMode)

    DisplayMode = DisplayMode
    core.Enum(DisplayMode)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._source_column = 0
        self._flattening_mode = FlatteningMode.Default
        self._display_mode = DisplayMode.Path
        self._source_root_index = core.ModelIndex()
        self._source_key: list[tuple[int, ...]] = []
        self._source_offset: dict[tuple[int, ...], int] = {}

    def setSourceModel(self, model):
        if (curr_model := self.sourceModel()) is not None:
            curr_model.dataChanged.disconnect(self._source_data_changed)
            curr_model.rowsInserted.disconnect(self._source_rows_inserted)
            curr_model.rowsRemoved.disconnect(self._source_rows_removed)
            curr_model.rowsMoved.disconnect(self._source_rows_moved)
        with self.reset_model():
            super().setSourceModel(model)
            self._update_row_mapping()

        model.dataChanged.connect(self._source_data_changed)
        model.rowsInserted.connect(self._source_rows_inserted)
        model.rowsRemoved.connect(self._source_rows_removed)
        model.rowsMoved.connect(self._source_rows_moved)

    def setSourceColumn(self, column: int):
        with self.reset_model():
            self._source_column = column
            self._update_row_mapping()

    def sourceColumn(self) -> int:
        return self._source_column

    def setSourceRootIndex(self, root_index: core.ModelIndex):
        with self.reset_model():
            self._source_root_index = root_index
            self._update_row_mapping()

    def sourceRootIndex(self) -> core.ModelIndex:
        return self._source_root_index

    def set_flattening_mode(self, mode: FlattenedTreeProxyModel.FlatteningMode):
        if mode != self._flattening_mode:
            with self.reset_model():
                self._flattening_mode = mode
                self._update_row_mapping()

    def get_flattening_mode(self) -> FlattenedTreeProxyModel.FlatteningMode:
        return self._flattening_mode

    def set_display_mode(self, mode: FlattenedTreeProxyModel.DisplayMode):
        if mode != self._display_mode:
            with self.reset_model():
                self._display_mode = mode

    def get_display_mode(self) -> FlattenedTreeProxyModel.DisplayMode:
        return self._display_mode

    def mapFromSource(self, source_index: core.ModelIndex) -> core.ModelIndex:
        if not source_index.isValid():
            return source_index
        key = self.get_index_key(source_index)
        offset = self._source_offset[key]
        row = offset + source_index.row()
        return self.index(row, 0)

    def mapToSource(self, index: core.ModelIndex) -> core.ModelIndex:
        if not index.isValid():
            return index
        row = index.row()
        source_key_path = self._source_key[row]
        return self.index_from_key(source_key_path)

    def index(
        self, row: int, column: int = 0, parent: core.ModelIndex | None = None
    ) -> core.ModelIndex:
        parent = parent or core.ModelIndex()
        return (
            core.ModelIndex()
            if parent.isValid()
            else self.createIndex(row, column, parent)  # object=row)
        )

    def parent(self, child=None) -> core.ModelIndex:
        return super().parent() if child is None else core.ModelIndex()

    def rowCount(self, parent=None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else len(self._source_key)

    def columnCount(self, parent=None) -> int:
        parent = parent or core.ModelIndex()
        return 0 if parent.isValid() else 1

    def flags(self, index):
        flags = super().flags(index)
        if self._flattening_mode != self.FlatteningMode.InternalNodesDisabled:
            return flags
        index = self.mapToSource(index)
        model = self.sourceModel()
        enabled = flags & QtCore.Qt.ItemFlag.ItemIsEnabled
        if model is not None and model.rowCount(index) > 0 and enabled:
            flags ^= QtCore.Qt.ItemFlag.ItemIsEnabled
        return flags

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.DISPLAY_ROLE and self._display_mode == DisplayMode.Path:
            index = self.mapToSource(index)
            model = self.sourceModel()
            path = model.get_breadcrumbs_path(index)
            return " / ".join(str(i) for i in path)
        return super().data(index, role)

    def _update_row_mapping(self):
        source = self.sourceModel()

        self._source_key = []
        self._source_offset = {}

        def create_mapping(model, index: core.ModelIndex, key_path: tuple[int, ...]):
            if (rowcount := model.rowCount(index)) > 0:
                if self._flattening_mode != self.FlatteningMode.LeavesOnly:
                    self._source_offset[key_path] = len(self._source_offset)
                    self._source_key.append(key_path)
                for i in range(rowcount):
                    create_mapping(model, model.index(i, 0, index), key_path + (i,))
            else:
                self._source_offset[key_path] = len(self._source_offset)
                self._source_key.append(key_path)

        if source is not None:
            for i in range(source.rowCount()):
                create_mapping(source, source.index(i, 0), (i,))

    def _source_data_changed(self, top, bottom):
        changed_indexes = [top.sibling(i, 0) for i in range(top.row(), bottom.row() + 1)]
        for ind in changed_indexes:
            self.dataChanged.emit(ind, ind)

    def _source_rows_inserted(self, parent: core.ModelIndex, start: int, end: int):
        with self.reset_model():
            self._update_row_mapping()

    def _source_rows_removed(self, parent: core.ModelIndex, start: int, end: int):
        with self.reset_model():
            self._update_row_mapping()

    def _source_rows_moved(
        self, source_parent, source_start, source_end, dest_parent, dest_row
    ):
        with self.reset_model():
            self._update_row_mapping()

    flatteningMode = core.Property(
        FlatteningMode,
        get_flattening_mode,
        set_flattening_mode,
    )

    displayMode = core.Property(
        DisplayMode,
        get_display_mode,
        set_display_mode,
    )


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    table = debugging.example_tree(flatten=True)
    table.show()
    app.main_loop()
