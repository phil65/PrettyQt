from __future__ import annotations

import numpy as np
import pandas as pd

from prettyqt import constants, core, gui, widgets

MAX_AUTOSIZE_MS = 150  # Milliseconds given (at most) to perform column auto-sizing
MIN_TRUNC_CHARS = 8  # Minimum size (in characters) given to columns
MAX_WIDTH_CHARS = 64  # Maximum size (in characters) given to columns

SelectionFlag = core.ItemSelectionModel.SelectionFlag


class ExtFrameModel:
    def __init__(self, data):
        super().__init__()
        self._data = data

    @property
    def shape(self):
        return self._data.shape

    @property
    def header_shape(self):
        return (len(self._data.columns.names), len(self._data.index.names))

    def data(self, y, x):
        return self._data.iat[y, x]

    def header(self, axis, x, level=0):
        ax = self._data.columns if axis == 0 else self._data.index
        return ax.values[x][level] if hasattr(ax, "levels") else ax.values[x]

    def name(self, axis, level):
        ax = self._data.columns if axis == 0 else self._data.index
        name = ax.names[level]
        return name if name is not None else f"L{str(level)}"


class Data4ExtModel(core.AbstractTableModel):
    def __init__(self, model):
        super().__init__()
        self._model = model

    def rowCount(self, index=None):
        return max(1, self._model.shape[0])

    def columnCount(self, index=None):
        return max(1, self._model.shape[1])

    def data(self, index, role):
        if index.row() >= self._model.shape[0] or index.column() >= self._model.shape[1]:
            return None
        match role:
            case constants.DISPLAY_ROLE:
                val = self._model.data(index.row(), index.column())
                return "" if pd.isnull(val) else str(val)


class Header4ExtModel(core.AbstractTableModel):
    def __init__(self, model, axis, palette):
        super().__init__()
        self._model = model
        self.axis = axis
        self._palette = palette
        if self.axis == 0:
            self._shape = (self._model.header_shape[0], self._model.shape[1])
        else:
            self._shape = (self._model.shape[0], self._model.header_shape[1])

    def rowCount(self, index=None):
        return max(1, self._shape[0])

    def columnCount(self, index=None):
        return max(1, self._shape[1])

    def headerData(self, section, orientation, role):
        match role, orientation:
            case constants.ALIGNMENT_ROLE, constants.HORIZONTAL:
                return constants.ALIGN_CENTER | constants.ALIGN_BOTTOM
            case constants.ALIGNMENT_ROLE, constants.VERTICAL:
                return constants.ALIGN_RIGHT | constants.ALIGN_V_CENTER
            case constants.DISPLAY_ROLE, constants.HORIZONTAL:
                return section if self.axis == 0 else self._model.name(1, section)
            case constants.DISPLAY_ROLE, constants.VERTICAL:
                return section if self.axis == 1 else self._model.name(0, section)

    def data(self, index, role):
        if (
            not index.isValid()
            or index.row() >= self._shape[0]
            or index.column() >= self._shape[1]
        ):
            return None
        row, col = (
            (index.row(), index.column())
            if self.axis == 0
            else (index.column(), index.row())
        )
        match role:
            case constants.BACKGROUND_ROLE:
                prev = self._model.header(self.axis, col - 1, row) if col else None
                cur = self._model.header(self.axis, col, row)
                return self._palette.midlight() if prev != cur else None
            case constants.DISPLAY_ROLE:
                val = self._model.header(self.axis, col, row)
                return "" if pd.isnull(val) else str(val)


class Level4ExtModel(core.AbstractTableModel):
    def __init__(self, model, palette, font):
        super().__init__()
        self._model = model
        self._background = palette.dark().color()
        if self._background.lightness() > 127:
            self._foreground = palette.text()
        else:
            self._foreground = palette.highlightedText()
        self._palette = palette
        font.setBold(True)
        self._font = font

    def rowCount(self, index=None):
        return max(1, self._model.header_shape[0])

    def columnCount(self, index=None):
        return max(1, self._model.header_shape[1])

    def headerData(self, section, orientation, role):
        match role, orientation:
            case constants.ALIGNMENT_ROLE, constants.HORIZONTAL:
                return constants.ALIGN_CENTER | constants.ALIGN_BOTTOM
            case constants.ALIGNMENT_ROLE, constants.VERTICAL:
                return constants.ALIGN_RIGHT | constants.ALIGN_V_CENTER
            case constants.DISPLAY_ROLE, _:
                return "L" + str(section)

    def data(self, index, role):
        if not index.isValid():
            return None
        a = self._model.header_shape[0] - 1
        b = self._model.header_shape[1] - 1
        match role:
            case constants.DISPLAY_ROLE if index.row() == a:
                return str(self._model.name(1, index.column()))
            case constants.DISPLAY_ROLE if index.column() == b:
                return str(self._model.name(0, index.row()))
            case constants.FOREGROUND_ROLE:
                return self._foreground
            case constants.BACKGROUND_ROLE:
                return self._background
            case constants.FONT_ROLE:
                return self._font


class DataFrameViewer(widgets.Widget):
    def __init__(self, df=None, parent=None):
        super().__init__(parent=parent)
        self._selection_rec = False
        self._model = None

        # We manually set the inactive highlight color to differentiate the
        # selection between the data/index/header. To actually make use of the
        # palette though, we also have to manually assign a new stock delegate
        # to each table view
        palette = self.get_palette()
        tmp = palette.highlight().color()
        tmp.setHsv(tmp.hsvHue(), 100, palette.midlight().color().lightness())
        palette.setBrush(
            gui.Palette.ColorGroup.Inactive, gui.Palette.ColorRole.Highlight, tmp
        )
        self.setPalette(palette)
        self.hscroll = widgets.ScrollBar("horizontal")
        self.vscroll = widgets.ScrollBar("vertical")

        self.table_level = widgets.TableView()
        self.table_level.set_edit_triggers("none")
        self.table_level.set_scrollbar_policy("always_off")
        self.table_level.set_frame_shadow("plain")
        self.table_level.h_header.sectionResized.connect(self._index_resized)
        self.table_level.v_header.sectionResized.connect(self._header_resized)
        self.table_level.set_delegate("variant")

        self.table_header = widgets.TableView()
        self.table_header.v_header.hide()
        self.table_header.set_edit_triggers("none")
        self.table_header.set_scrollbar_policy("always_off")
        self.table_header.set_horizontal_scroll_mode("pixel")
        self.table_header.setHorizontalScrollBar(self.hscroll)
        self.table_header.set_frame_shadow("plain")
        self.table_header.h_header.sectionResized.connect(self._column_resized)
        self.table_header.set_delegate("variant")

        self.table_index = widgets.TableView()
        self.table_index.h_header.hide()
        self.table_index.set_edit_triggers("none")
        self.table_index.set_scrollbar_policy("always_off")
        self.table_index.set_vertical_scroll_mode("pixel")
        self.table_index.setVerticalScrollBar(self.vscroll)
        self.table_index.set_frame_shadow("plain")
        self.table_index.v_header.sectionResized.connect(self._row_resized)

        self.table_data = widgets.TableView()
        self.table_data.v_header.hide()
        self.table_data.h_header.hide()
        self.table_data.set_edit_triggers("none")
        self.table_data.set_scrollbar_policy("always_off")
        self.table_data.set_scroll_mode("pixel")
        self.table_data.setHorizontalScrollBar(self.hscroll)
        self.table_data.setVerticalScrollBar(self.vscroll)
        self.table_data.set_frame_shadow("plain")
        self.table_data.set_delegate("variant")
        layout = self.set_layout("grid", spacing=0, margin=0)
        layout[0, 0] = self.table_level
        layout[0, 1] = self.table_header
        layout[1, 0] = self.table_index
        layout[1, 1] = self.table_data
        layout[2, 1] = self.hscroll
        layout[1, 2] = self.vscroll
        # layout.addWidget(self.hscroll, 2, 0, 2, 2)
        # layout.addWidget(self.vscroll, 0, 2, 2, 2)
        self.setFocusProxy(self.table_data)

        # autosize columns on-demand
        self._autosized_cols = set()
        self._max_autosize_ms = MAX_AUTOSIZE_MS
        self.hscroll.sliderMoved.connect(self._resize_visible_columns_to_contents)
        self.table_data.installEventFilter(self)

        avg_width = self.fontMetrics().averageCharWidth()
        self.min_trunc = avg_width * MIN_TRUNC_CHARS
        self.max_width = avg_width * MAX_WIDTH_CHARS
        if df is not None:
            self.set_df(df)

    def set_df(self, df):
        model = ExtFrameModel(df)
        self.set_model(model)

    def _select_columns(self, source, dest, deselect):
        if self._selection_rec:
            return
        self._selection_rec = True
        dsm = dest.selectionModel()
        ssm = source.selectionModel()
        dsm.clear()
        for col in (index.column() for index in ssm.selectedIndexes()):
            idx = dest.model().index(0, col)
            dsm.select(idx, SelectionFlag.Select | SelectionFlag.Columns)
        deselect.selectionModel().clear()
        self._selection_rec = False

    def _select_rows(self, source, dest, deselect):
        if self._selection_rec:
            return
        self._selection_rec = True
        dsm = dest.selectionModel()
        dsm.clear()
        for row in (index.row() for index in source.selectionModel().selectedIndexes()):
            idx = dest.model().index(row, 0)
            dsm.select(idx, SelectionFlag.Select | SelectionFlag.Rows)
        deselect.selectionModel().clear()
        self._selection_rec = False

    def model(self):
        return self._model

    def _column_resized(self, col, old_width, new_width):
        self.table_data.setColumnWidth(col, new_width)
        self._update_layout()

    def _row_resized(self, row, old_height, new_height):
        self.table_data.setRowHeight(row, new_height)
        self._update_layout()

    def _index_resized(self, col, old_width, new_width):
        self.table_index.setColumnWidth(col, new_width)
        self._update_layout()

    def _header_resized(self, row, old_height, new_height):
        self.table_header.setRowHeight(row, new_height)
        self._update_layout()

    def _update_layout(self):
        h_width = max(
            self.table_level.v_header.sizeHint().width(),
            self.table_index.v_header.sizeHint().width(),
        )
        self.table_level.v_header.setFixedWidth(h_width)
        self.table_index.v_header.setFixedWidth(h_width)

        last_row = self._model.header_shape[0] - 1
        if last_row < 0:
            hdr_height = self.table_level.h_header.height()
        else:
            hdr_height = (
                self.table_level.rowViewportPosition(last_row)
                + self.table_level.rowHeight(last_row)
                + self.table_level.h_header.height()
            )
        self.table_header.setFixedHeight(hdr_height)
        self.table_level.setFixedHeight(hdr_height)

        last_col = self._model.header_shape[1] - 1
        if last_col < 0:
            idx_width = self.table_level.v_header.width()
        else:
            idx_width = (
                self.table_level.columnViewportPosition(last_col)
                + self.table_level.columnWidth(last_col)
                + self.table_level.v_header.width()
            )
        self.table_index.setFixedWidth(idx_width)
        self.table_level.setFixedWidth(idx_width)
        self._resize_visible_columns_to_contents()

    def set_auto_size_limit(self, limit_ms):
        self._max_autosize_ms = limit_ms

    def set_model(self, model, relayout=True):
        self._model = model
        data_model = Data4ExtModel(model)
        self.table_data.set_model(data_model)
        sel_model = self.table_data.selectionModel()
        sel_model.selectionChanged.connect(
            lambda *_: self._select_columns(
                self.table_data, self.table_header, self.table_level
            )
        )
        sel_model.selectionChanged.connect(
            lambda *_: self._select_rows(
                self.table_data, self.table_index, self.table_level
            )
        )
        sel_model.currentColumnChanged.connect(self._resize_current_column_to_content)

        level_model = Level4ExtModel(model, self.palette(), self.font())
        self.table_level.set_model(level_model)
        sel_model = self.table_level.selectionModel()
        sel_model.selectionChanged.connect(
            lambda *_: self._select_columns(
                self.table_level, self.table_index, self.table_data
            )
        )
        sel_model.selectionChanged.connect(
            lambda *_: self._select_rows(
                self.table_level, self.table_header, self.table_data
            )
        )

        header_model = Header4ExtModel(model, 0, self.palette())
        self.table_header.set_model(header_model)
        sel_model = self.table_header.selectionModel()
        sel_model.selectionChanged.connect(
            lambda *_: self._select_columns(
                self.table_header, self.table_data, self.table_index
            )
        )
        sel_model.selectionChanged.connect(
            lambda *_: self._select_rows(
                self.table_header, self.table_level, self.table_index
            )
        )

        index_model = Header4ExtModel(model, 1, self.palette())
        self.table_index.set_model(index_model)
        sel_model = self.table_index.selectionModel()
        sel_model.selectionChanged.connect(
            lambda *_: self._select_rows(
                self.table_index, self.table_data, self.table_header
            )
        )
        sel_model.selectionChanged.connect(
            lambda *_: self._select_columns(
                self.table_index, self.table_level, self.table_header
            )
        )

        # needs to be called after setting all table models
        if relayout:
            self._update_layout()

    def setCurrentIndex(self, y, x):
        self.table_data.selectionModel().setCurrentIndex(
            self.table_data.model().index(y, x),
            SelectionFlag.ClearAndSelect,
        )

    def _resize_column_to_contents(self, header, data, col, limit_ms: int):
        hdr_width = header.get_size_hint_for_column(col, limit_ms)
        data_width = data.get_size_hint_for_column(col, limit_ms)
        if data_width > hdr_width:
            width = min(self.max_width, data_width)
        elif hdr_width > data_width * 2:
            width = max(min(hdr_width, self.min_trunc), min(self.max_width, data_width))
        else:
            width = min(self.max_width, hdr_width)
        header.setColumnWidth(col, width)

    def _resize_columns_to_contents(self, header, data, limit_ms: int):
        max_col = data.model().columnCount()
        max_col_ms = None if limit_ms is None else limit_ms / max(1, max_col)
        for col in range(max_col):
            self._resize_column_to_contents(header, data, col, max_col_ms)

    def eventFilter(self, obj, event):
        if obj == self.table_data and event.type() == core.Event.Type.Resize:
            self._resize_visible_columns_to_contents()
        return False

    def _resize_visible_columns_to_contents(self):
        start = col = self.table_data.columnAt(self.table_data.rect().topLeft().x())
        width = self._model.shape[1]
        end = self.table_data.columnAt(self.table_data.rect().bottomRight().x())
        end = width if end == -1 else end + 1
        if self._max_autosize_ms is None:
            max_col_ms = None
        else:
            max_col_ms = self._max_autosize_ms / max(1, end - start)
        while col < end:
            resized = False
            if col not in self._autosized_cols:
                self._autosized_cols.add(col)
                resized = True
                self._resize_column_to_contents(
                    self.table_header, self.table_data, col, max_col_ms
                )
            col += 1
            if resized:
                # as we resize columns, the boundary will change
                end = self.table_data.columnAt(self.table_data.rect().bottomRight().x())
                end = width if end == -1 else end + 1
                if max_col_ms is not None:
                    max_col_ms = self._max_autosize_ms / max(1, end - start)

    def _resize_current_column_to_content(self, new_index, old_index):
        if new_index.column() not in self._autosized_cols:
            # ensure the requested column is fully into view after resizing
            self._resize_visible_columns_to_contents()
            self.table_data.scrollTo(new_index)

    def resizeColumnsToContents(self):
        self._autosized_cols = set()
        self._resize_columns_to_contents(
            self.table_level, self.table_index, self._max_autosize_ms
        )
        self._update_layout()


if __name__ == "__main__":
    tuples = [
        ("bar", "one", "q"),
        ("bar", "two", "q"),
        ("baz", "one", "q"),
        ("baz", "two", "q"),
        ("foo", "one", "q"),
        ("foo", "two", "q"),
        ("qux", "one", "q"),
        ("qux", "two", "q"),
    ]
    index = pd.MultiIndex.from_tuples(tuples, names=["first", "second", "third"])
    df = pd.DataFrame(np.random.randn(8, 8), index=index, columns=index)
    app = widgets.app()
    table = DataFrameViewer()
    table.set_df(df)
    table.resizeColumnsToContents()
    table.show()
    app.main_loop()
