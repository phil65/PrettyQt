from __future__ import annotations

import logging
import threading

import pandas as pd
import numpy as np

from prettyqt import constants, custom_widgets, core, gui, widgets
from prettyqt.qt import QtCore, QtGui
from prettyqt.qtpandas import pandasmodels

logger = logging.getLogger(__name__)

SelectionFlag = core.ItemSelectionModel.SelectionFlag


class DataTableView(widgets.TableView):
    def __init__(self, df=None, **kwargs):
        super().__init__(**kwargs)

        self.h_header.hide()
        self.v_header.hide()
        self.setAlternatingRowColors(True)
        self.set_scroll_mode("pixel")
        self.set_margin(0)
        self.set_delegate("no_focus")
        self.set_scrollbar_policy("always_off")
        self.set_delegate("variant")
        self.set_size_policy("expanding", "expanding")
        self.set_df(df)

    def set_df(self, df: pd.DataFrame):
        model = pandasmodels.DataTableModel(df, parent=self)
        self.set_model(model)

    def copy(self):
        indexes = self.selectionModel().selection().indexes()

        rows = [ix.row() for ix in indexes]
        cols = [ix.column() for ix in indexes]

        df = self.get_model(skip_proxies=True).df
        df = df.iloc[min(rows) : max(rows) + 1, min(cols) : max(cols) + 1]
        kwargs = dict(index=False, header=False)
        threading.Thread(target=df.to_clipboard, kwargs=kwargs).start()

    def paste(self):
        app = widgets.app()
        clipboard = app.clipboard()
        # TODO
        print(clipboard.text())

    def sizeHint(self):
        if self.get_model(skip_proxies=True).df is None:
            return core.Size(0, 0)
        width = 2 * self.frameWidth()  # Account for border & padding
        # width += self.v_scrollbar.width()
        max_cols = min(100, self.model().columnCount())
        for i in range(max_cols):
            width += self.columnWidth(i)

        # Height
        height = 2 * self.frameWidth()  # Account for border & padding
        # height += self.h_scrollbar.height()
        max_rows = min(100, self.model().rowCount())
        for i in range(max_rows):
            height += self.rowHeight(i)

        return core.Size(width, height)


class DataFrameViewer(widgets.Widget):
    def __init__(self, df: pd.DataFrame | None = None, **kwargs):
        super().__init__(**kwargs)
        # Indicates whether the widget has been shown yet. Set to True in
        self._loaded = False
        self.df = df
        # Set up DataFrame TableView and Model
        self.table_data = DataTableView(df, parent=self)
        self.set_size_policy("expanding", "expanding")

        self.table_data.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )
        # Create headers
        self.table_columns = HeaderView(orientation=constants.HORIZONTAL, parent=self)
        self.table_columns.clicked.connect(self.on_clicked)

        self.table_index = HeaderView(orientation=constants.VERTICAL, parent=self)

        # Set up layout
        self.layout_grid = self.set_layout("grid", margin=0, spacing=0)
        # Link scrollbars
        self.table_data.h_scrollbar.valueChanged.connect(
            self.table_columns.h_scrollbar.setValue
        )
        self.table_data.v_scrollbar.valueChanged.connect(
            self.table_index.v_scrollbar.setValue
        )
        self.table_columns.h_scrollbar.valueChanged.connect(
            self.table_data.h_scrollbar.setValue
        )
        self.table_index.v_scrollbar.valueChanged.connect(
            self.table_data.v_scrollbar.setValue
        )

        # Disable scrolling on the headers. Even when hidden, dragging desyncs them
        self.table_index.h_scrollbar.valueChanged.connect(lambda: None)

        # Add items to layout

        # SpacerItem |            Table_columns
        #       table index             | TrackingSpacer
        #       Table Index             | Table Data      | V Scrollbar
        #            |  Tracking Spacer  |H Scrollbar
        self.layout_grid[0, 0] = widgets.SpacerItem(0, 0, "expanding", "expanding")
        self.layout_grid[0, 1:2] = self.table_columns
        self.layout_grid[1:2, 0:1] = self.table_index
        self.layout_grid[1, 2] = TrackingSpacer(ref_y=self.table_index.h_header)
        self.layout_grid[2, 2] = self.table_data
        self.layout_grid[2, 3] = self.table_data.v_scrollbar
        self.layout_grid[3, 1] = TrackingSpacer(ref_x=self.table_columns.v_header)
        self.layout_grid[3, 2] = self.table_data.h_scrollbar

        # These expand when the window is enlarged instead of having
        # the grid squares spread out
        self.layout_grid.setColumnStretch(4, 1)
        self.layout_grid.setRowStretch(4, 1)

        # These placeholders will ensure the size of the blank spaces beside our headers
        if df is not None:
            self.set_df(df)

    def set_df(self, df: pd.DataFrame):
        self.df = df
        model = pandasmodels.DataTableModel(df, parent=self.table_data)
        self.table_data.set_model(model)

        self.table_data.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )
        # TODO: this gets called twice.
        self.table_columns.set_df(df)
        self.table_index.set_df(df)
        # Toggle level names
        if not (any(df.columns.names) or df.columns.name):
            self.table_columns.v_header.setFixedWidth(0)
        if not (any(df.index.names) or df.index.name):
            self.table_index.h_header.setFixedHeight(0)
        self.table_columns.selectionModel().selectionChanged.connect(
            self.on_column_selection_changed
        )
        self.table_index.selectionModel().selectionChanged.connect(
            self.on_index_selection_changed
        )
        self._resize_columns()
        self.table_data.updateGeometry()
        self.table_columns.updateGeometry()

    def jump_to_column(self, col_num: int):
        """Make sure column at given index is visible.

        Scrolls to column at given index.

        Arguments:
            col_num: column to scroll to
        """
        if (model := self.table_data.model()) is not None:
            idx = model.index(0, col_num)
            self.table_data.scrollTo(idx)
        if (model := self.table_index.model()) is not None:
            idx = model.index(0, col_num)
            self.table_index.scrollTo(idx)
        if (model := self.table_columns.model()) is not None:
            idx = model.index(0, col_num)
            self.table_columns.scrollTo(idx)

    # def on_column_selection_changed(self, selected, deselected):
    #     if self.table_columns.hasFocus():
    #         selected = self.table_columns.get_higher_levels()
    #         self.table_data.selectionModel().select(
    #             selected,
    #             SelectionFlag.Columns
    #             | SelectionFlag.ClearAndSelect,
    #         )
    #     self.table_columns._on_selection_changed(selected, deselected)

    # def on_index_selection_changed(self, selected, deselected):
    #     if not self.table_index.hasFocus():
    #         return
    #     selected = self.table_index.get_higher_levels()
    #     self.table_data.selectionModel().select(
    #         selected,
    #         SelectionFlag.Rows
    #         | SelectionFlag.ClearAndSelect,
    #     )
    #     self.table_index._on_selection_changed(selected, deselected)

    def on_clicked(self, ix: QtCore.QModelIndex):
        self.df = self.df.sort_values(self.df.columns[ix.column()])
        self.data_changed()

    def showEvent(self, event: QtGui.QShowEvent):
        """Initialize column and row sizes on the first time the widget is shown."""
        if not self._loaded and self.df is not None:
            # Set column widths
            self._resize_columns()

            self._loaded = True
        event.accept()

    def _resize_columns(self):
        N = 50
        columns = min(self.table_index.model().columnCount(), N)
        for column_index in range(columns):
            self.auto_size_column(column_index)

        # Set row heights
        # Just sets a single uniform row height based on the first
        # N rows for performance.
        default_row_height = 30
        rows = min(self.table_index.model().rowCount(), N)
        for row_index in range(rows):
            self.auto_size_row(row_index)
            height = self.table_index.rowHeight(row_index)
            default_row_height = max(default_row_height, height)

        # Set limit for default row height
        default_row_height = min(default_row_height, 100)

        self.table_index.v_header.setDefaultSectionSize(default_row_height)
        self.table_data.v_header.setDefaultSectionSize(default_row_height)

    def on_column_selection_changed(self, selected, deselected):
        if not self.table_columns.hasFocus():
            return
        higher_levels = self.table_columns.get_higher_levels()
        # Set selection mode so selecting one row or column at a time
        # adds to selection each time
        selected.merge(higher_levels, SelectionFlag.Deselect)
        # Select the cells in the data view
        self.table_data.selectionModel().select(
            selected, SelectionFlag.Columns | SelectionFlag.ClearAndSelect
        )

    def on_index_selection_changed(self, selected, deselected):
        if not self.table_index.hasFocus():
            return
        higher_levels = self.table_index.get_higher_levels()
        selected.merge(higher_levels, SelectionFlag.Deselect)
        self.table_data.selectionModel().select(
            selected, SelectionFlag.Rows | SelectionFlag.ClearAndSelect
        )

    def _on_selection_changed(self, selected, deselected):
        """Runs when cells are selected in the main table.

        This logic highlights the correct
        cells in the vertical and horizontal headers when a data cell is selected
        """
        # The two blocks below check what columns or rows are selected in the data table
        # and highlights thecorresponding ones in the two headers. The if statements
        # check for focus on headers, because if the user clicks a header that will
        # auto-select all cells in that row or column which will trigger this function
        # and cause and infinite loop

        if not self.table_columns.hasFocus():
            self.table_columns.selectionModel().select(
                selected, SelectionFlag.Columns | SelectionFlag.ClearAndSelect
            )

        if not self.table_index.hasFocus():
            self.table_index.selectionModel().select(
                selected, SelectionFlag.Rows | SelectionFlag.ClearAndSelect
            )

    def auto_size_column(self, column_index: int):
        """Set the size of column at column_index to fit its contents."""
        padding = 20

        self.table_columns.resizeColumnToContents(column_index)
        width = self.table_columns.columnWidth(column_index)

        # Iterate over the column's rows and check the width of each
        # to determine the max width for the column
        # Only check the first N rows for performance. If there is larger
        # content in cells below it will be cut off
        N = 75
        rows = min(self.table_data.model().rowCount(), N)
        for i in range(rows):
            mi = self.table_data.model().index(i, column_index)
            text = self.table_data.model().data(mi)
            text = str(text)  # TODO: get rid of casting?
            w = self.table_data.fontMetrics().boundingRect(text).width()

            width = max(width, w)

        width += padding

        # add maximum allowable column width so column is never too big.
        max_allowable_width = 400
        width = min(width, max_allowable_width)

        self.table_columns.setColumnWidth(column_index, width)
        self.table_data.setColumnWidth(column_index, width)

        self.table_data.updateGeometry()
        self.table_columns.updateGeometry()

    def auto_size_row(self, row_index: int):
        """Set the size of row at row_index to fix its contents."""
        padding = 20

        self.table_index.resizeRowToContents(row_index)
        height = self.table_index.rowHeight(row_index)

        # Iterate over the row's columns and check the width of each to
        # determine the max height for the row
        # Only check the first N columns for performance.
        N = 100
        model = self.table_data.model()
        for i in range(min(N, model.columnCount())):
            mi = model.index(row_index, i)
            cell_width = self.table_columns.columnWidth(i)
            text = model.data(mi)
            # Gets row height at a constrained width (the column width).
            # This constrained width, with the flag of Qt.TextWordWrap
            # gets the height the cell would have to be to fit the text.
            constrained_rect = core.Rect(0, 0, cell_width, 0)
            text = str(text)  # TODO: remove this?
            h = (
                self.table_data.fontMetrics()
                .boundingRect(constrained_rect, QtCore.Qt.TextFlag.TextWordWrap, text)
                .height()
            )

            height = max(height, h)

        height += padding

        self.table_index.setRowHeight(row_index, height)
        self.table_data.setRowHeight(row_index, height)

        self.table_data.updateGeometry()
        self.table_index.updateGeometry()

    def keyPressEvent(self, event: core.QEvent):
        super().keyPressEvent(event)

        if event.matches(gui.KeySequence.StandardKey.Copy):
            self.table_data.copy()
        elif event.matches(gui.KeySequence.StandardKey.Paste):
            self.table_data.paste()

    def data_changed(self):
        # Call dataChanged on all models for all data
        for model in [
            self.table_data.model(),
            self.table_columns.model(),
            self.table_index.model(),
        ]:
            model.update_all()


class HeaderView(custom_widgets.OrientedTableView):
    """Displays the DataFrame index or columns depending on orientation."""

    def __init__(self, parent: DataFrameViewer, orientation: constants.Orientation):
        super().__init__(orientation, parent=parent)

        self.table = parent.table_data
        # These are used during column resizing
        self._header_is_resizing = None
        self.resize_start_pos: int | None = None
        self.initial_header_size = None

        # Handled by self.eventFilter()
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

        # Settings
        self.set_size_policy("maximum", "maximum")
        self.setWordWrap(False)
        self.set_horizontal_scrollbar_policy("always_off")
        self.set_scroll_mode("pixel")
        self.set_margin(0)
        self.set_delegate("no_focus")

        # Orientation specific settings
        if self.is_horizontal():
            self.set_horizontal_scrollbar_policy("always_off")
            self.h_header.hide()
            self.v_header.setDisabled(True)
            # Selection lags without this
            self.v_header.setHighlightSections(False)

        else:
            self.set_vertical_scrollbar_policy("always_off")
            self.v_header.hide()
            self.h_header.setDisabled(True)
            self.h_header.setHighlightSections(False)
        df = parent.df
        if df is not None:
            self.set_df(df)
            self.resize(self.sizeHint())

    def set_df(self, df: pd.DataFrame, set_spans: bool = True):
        if self.is_horizontal():
            model = pandasmodels.HorizontalHeaderModel(df)
        else:
            model = pandasmodels.VerticalHeaderModel(df)
        self.set_model(model)
        # Link selection to DataTable
        if set_spans:
            self.set_spans()
        self.init_size()
        # Set initial size
        self.resize(self.sizeHint())

    def get_higher_levels(self):
        model = self.model()
        if self.is_horizontal():
            # Get the header's selected columns
            # Removes the higher levels so that only the lowest level of the header
            # affects the data table selection
            last_row_ix = model.df.columns.nlevels - 1
            last_col_ix = model.columnCount() - 1
            return core.ItemSelection(
                model.index(0, 0), model.index(last_row_ix - 1, last_col_ix)
            )
        else:
            last_row_ix = model.rowCount() - 1
            last_col_ix = model.df.index.nlevels - 1
            return core.ItemSelection(
                model.index(0, 0), model.index(last_row_ix, last_col_ix - 1)
            )

    # Take the current set of selected cells and make it so that any spanning cell above
    # a selected cell is selected too This should happen after every selection change
    def selectionChanged(self, selected, deselected):
        if self.is_horizontal():
            if self.get_model(skip_proxies=True).df.columns.nlevels == 1:
                return
            for ix in self.selectedIndexes():
                for row in range(ix.row()):
                    ix2 = self.model().index(row, ix.column())
                    self.setSelection(self.visualRect(ix2), SelectionFlag.Select)
        else:
            if self.get_model(skip_proxies=True).df.index.nlevels == 1:
                return
            for ix in self.selectedIndexes():
                for col in range(ix.column()):
                    ix2 = self.model().index(ix.row(), col)
                    self.setSelection(self.visualRect(ix2), SelectionFlag.Select)

    # Fits columns to contents but with a minimum width and added padding
    def init_size(self):
        padding = 20
        self.resizeColumnsToContents()
        colcount = min(self.model().columnCount(), 100)
        if self.is_horizontal():
            min_size = 100
            for col in range(colcount):
                width = self.columnWidth(col)
                new_width = max(width + padding, min_size)
                self.setColumnWidth(col, new_width)
                self.table.setColumnWidth(col, new_width)
        else:
            # max_size = 1000
            for col in range(colcount):
                width = self.columnWidth(col)
                self.setColumnWidth(col, width + padding)

    # This sets spans to group together adjacent cells with the same values
    def set_spans(self):
        df = self.get_model(skip_proxies=True).df
        index = df.columns if self.is_horizontal() else df.index
        is_multiindex = isinstance(index, pd.MultiIndex)
        n = len(index[0]) if is_multiindex else 1
        for level in range(n):
            # Find how many segments the MultiIndex has
            arr = index.codes[level] if is_multiindex else index
            starts = np.where(arr[:-1] != arr[1:])[0] + 1
            starts = np.insert(starts, 0, 0)
            lengths = np.diff(starts)
            lengths = np.append(lengths, len(arr) - starts[-1])
            for start, length in zip(starts, lengths):
                if length > 1:
                    self.set_section_span(level, start, length)
            # Holds the starting index of a range of equal values.
            # None means it is not currently in a range of equal values.
            # match_start = None
            # for col in range(1, len(arr)):  # Iterates over cells in row
            #     # Check if cell matches cell to its left
            #     if arr[col] == arr[col - 1]:
            #         if match_start is None:
            #             match_start = col - 1
            #         # If this is the last cell, need to end it
            #         if col == len(arr) - 1:
            #             match_end = col
            #             span_size = match_end - match_start + 1
            #             self.set_section_span(level, match_start, span_size)
            #     elif match_start is not None:
            #         match_end = col - 1
            #         span_size = match_end - match_start + 1
            #         self.set_section_span(level, match_start, span_size)
            #         match_start = None

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent):
        if not isinstance(event, QtGui.QMouseEvent):
            return False
        mouse_pos = event.position().x() if self.is_horizontal() else event.position().y()
        mouse_pos = int(mouse_pos)
        # If mouse is on an edge, start the drag resize process
        match event.type():
            case QtCore.QEvent.Type.MouseButtonPress:
                if self.over_header_edge(mouse_pos) is not None:
                    self._header_is_resizing = self.over_header_edge(mouse_pos)
                    self.resize_start_pos = mouse_pos
                    self.initial_header_size = self.sectionWidth(self._header_is_resizing)
                    return True
                else:
                    self._header_is_resizing = None
            # End the drag process
            case QtCore.QEvent.Type.MouseButtonRelease:
                self._header_is_resizing = None

            case QtCore.QEvent.Type.MouseButtonDblClick if self.is_horizontal():
                if (header_index := self.over_header_edge(mouse_pos)) is not None:
                    self.parent().auto_size_column(header_index)
                    return True

            case QtCore.QEvent.Type.MouseButtonDblClick:
                if (header_index := self.over_header_edge(mouse_pos)) is not None:
                    self.parent().auto_size_row(header_index)
                    return True
            case QtCore.QEvent.Type.MouseMove:
                # If this is None, there is no drag resize happening
                if self._header_is_resizing is not None:
                    size = self.initial_header_size + mouse_pos - self.resize_start_pos
                    if size > 10:
                        table_data = self.parent().table_data
                        self.setSectionWidth(self._header_is_resizing, size)
                        if self.is_horizontal():
                            table_data.setColumnWidth(self._header_is_resizing, size)
                        else:
                            table_data.setRowHeight(self._header_is_resizing, size)
                        self.updateGeometry()
                        table_data.updateGeometry()
                    return True

                # Set the cursor shape
                if self.over_header_edge(mouse_pos) is not None:
                    self.viewport().setCursor(self.get_split_cursor())
                else:
                    cursor = gui.Cursor(QtCore.Qt.CursorShape.ArrowCursor)
                    self.viewport().setCursor(cursor)
        return False

    # Return the size of the header needed to match the corresponding DataTableView
    def sizeHint(self):
        if self.model() is None:
            return core.Size(0, 0)
        # Horizontal HeaderView
        if self.is_horizontal():
            # Width of DataTableView
            width = self.table.sizeHint().width() + self.v_header.width()
            # Height
            height = 2 * self.frameWidth()  # Account for border & padding
            max_rows = min(100, self.model().rowCount())
            for i in range(max_rows):
                height += self.rowHeight(i)

        # Vertical HeaderView
        else:
            # Height of DataTableView
            height = self.table.sizeHint().height() + self.h_header.height()
            # Width
            width = 2 * self.frameWidth()  # Account for border & padding
            max_cols = min(100, self.model().columnCount())
            for i in range(max_cols):
                width += self.columnWidth(i)
        return core.Size(width, height)

    # This is needed because otherwise when the horizontal header is a single row
    # it will add whitespace to be bigger
    def minimumSizeHint(self):
        if self.is_horizontal():
            return core.Size(0, self.sizeHint().height())
        else:
            return core.Size(self.sizeHint().width(), 0)


# This is a fixed size widget with a size that tracks some other widget
class TrackingSpacer(widgets.Frame):
    def __init__(self, ref_x=None, ref_y=None):
        super().__init__()
        self.ref_x = ref_x
        self.ref_y = ref_y

    def minimumSizeHint(self):
        width = self.ref_x.width() if self.ref_x else 0
        height = self.ref_y.height() if self.ref_y else 0
        return core.Size(width, height)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()
    df = debugging.example_multiindex_df()
    with app.debug_mode():
        view2 = DataFrameViewer(df)
        view2.show()
        app.main_loop()
