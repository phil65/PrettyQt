# credits to https://github.com/glourencoffee/pyqt5span

from __future__ import annotations

from typing import Any
import enum

from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt import constants, core, widgets

SECTION_HEIGHT = 40
SECTION_WIDTH = 50


class _SpanHeaderItem:
    """Stores data of an index of `SpanHeaderModel`."""

    __slots__ = ("_row", "_column", "_parent", "_children", "_data")

    def __init__(
        self, row: int = 0, column: int = 0, parent: _SpanHeaderItem | None = None
    ):
        self._row = row
        self._column = column
        self._parent = parent
        self._children = {}
        self._data = {}

    def insertChild(self, row: int, col: int) -> _SpanHeaderItem:
        child = _SpanHeaderItem(row, col, self)
        self._children[(row, col)] = child
        return child

    def child(self, row: int, col: int) -> _SpanHeaderItem | None:
        return self._children.get((row, col), None)

    def parent(self) -> _SpanHeaderItem | None:
        return self._parent

    def row(self) -> int:
        return self._row

    def column(self) -> int:
        return self._column

    def setData(self, data: Any, role: int) -> None:
        self._data[role] = data

    def data(self, role: int) -> Any:
        return self._data.get(role, None)

    def clear(self) -> None:
        for child in self._children.values():
            child.clear()

        self._children.clear()


class SpanHeaderModel(core.AbstractTableModel):
    class HeaderRole(enum.IntEnum):
        """Roles for header."""

        ColumnSpanRole = constants.USER_ROLE + 1
        RowSpanRole = ColumnSpanRole + 1

    def __init__(self, rows: int, columns: int, parent: Any | None = None):
        super().__init__(parent)

        self._rows = rows
        self._columns = columns
        self._root_item = _SpanHeaderItem()

    def index(
        self, row: int, column: int, parent: QtCore.QModelIndex | None = None
    ) -> QtCore.QModelIndex:
        parent = parent or QtCore.QModelIndex()
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item: _SpanHeaderItem = parent.internalPointer()

        child_item = parent_item.child(row, column)

        if child_item is None:
            child_item = parent_item.insertChild(row, column)

        return self.createIndex(row, column, child_item)

    def rowCount(self, parent: QtCore.QModelIndex | None = None) -> int:
        return self._rows

    def columnCount(self, parent: QtCore.QModelIndex | None = None) -> int:
        return self._columns

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        if not index.isValid():
            return QtCore.Qt.ItemFlag.NoItemFlags

        return super().flags(index)

    def data(self, index: QtCore.QModelIndex, role: int) -> Any:
        if not index.isValid():
            return None

        if (
            index.row() >= self._rows
            or index.row() < 0
            or index.column() >= self._columns
            or index.column() < 0
        ):
            return None

        item: _SpanHeaderItem = index.internalPointer()

        return item.data(role)

    def setData(
        self,
        index: QtCore.QModelIndex,
        value: Any,
        role: int = QtCore.Qt.ItemDataRole.EditRole,
    ) -> bool:
        if index.isValid():
            item: _SpanHeaderItem = index.internalPointer()

            if role == SpanHeaderModel.HeaderRole.ColumnSpanRole:
                col = index.column()
                span: int = value

                if span > 0:
                    if col + span - 1 >= self._columns:
                        span = self._columns - col

                    item.setData(span, SpanHeaderModel.HeaderRole.ColumnSpanRole)

            elif role == SpanHeaderModel.HeaderRole.RowSpanRole:
                row = index.row()
                span: int = value

                if span > 0:
                    if row + span - 1 > self._rows:
                        span = self._rows - row

                    item.setData(span, SpanHeaderModel.HeaderRole.RowSpanRole)

            else:
                item.setData(value, role)

            return True

        return False

    def insertRows(
        self, row: int, count: int, parent: QtCore.QModelIndex | None = None
    ) -> bool:
        parent = parent or QtCore.QModelIndex()
        with self.insert_rows(row, row + count - 1, parent):
            self._rows += count
        return True

    def removeRows(
        self, row: int, count: int, parent: QtCore.QModelIndex | None = None
    ) -> bool:
        parent = parent or QtCore.QModelIndex()
        with self.remove_rows(row, row + count - 1, parent):
            self._rows -= count
        return True

    def insertColumns(
        self, column: int, count: int, parent: QtCore.QModelIndex | None = None
    ) -> bool:
        parent = parent or QtCore.QModelIndex()
        with self.insert_columns(column, column + count - 1, parent):
            self._columns += count
        return True

    def removeColumns(
        self, column: int, count: int, parent: QtCore.QModelIndex | None = None
    ) -> bool:
        parent = parent or QtCore.QModelIndex()
        with self.remove_columns(column, column + count - 1, parent):
            self._columns -= count
        return True


class SpanHeaderView(widgets.HeaderView):
    sectionPressed = core.Signal(int, int)

    def __init__(
        self,
        orientation: QtCore.Qt.Orientation,
        sections: int = 0,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(orientation, parent)

        base_section_size = QtCore.QSize()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            base_section_size.setWidth(self.defaultSectionSize())
            base_section_size.setHeight(SECTION_HEIGHT / 2)
            rows = 1
            columns = sections
        else:
            base_section_size.setWidth(SECTION_WIDTH)
            base_section_size.setHeight(self.defaultSectionSize())
            rows = sections
            columns = 1

        model = SpanHeaderModel(rows, columns)
        self.setModel(model)

        for row in range(rows):
            for col in range(columns):
                model.setData(
                    model.index(row, col),
                    base_section_size,
                    QtCore.Qt.ItemDataRole.SizeHintRole,
                )

        self.sectionResized.connect(self.onSectionResized)

    def setSectionCount(self, sections: int) -> None:
        model = self.model()

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            current_sections = model.columnCount()

            if sections < current_sections:
                model.removeColumns(sections, current_sections - sections)
            elif sections > current_sections:
                model.insertColumns(current_sections, sections - current_sections)

                for col in range(current_sections, sections):
                    model.setData(
                        model.index(0, col),
                        QtCore.QSize(self.defaultSectionSize(), SECTION_HEIGHT),
                        QtCore.Qt.ItemDataRole.SizeHintRole,
                    )
        else:
            current_sections = model.rowCount()

            if sections < current_sections:
                model.removeRows(sections, current_sections - sections)
            elif sections > current_sections:
                model.insertRows(current_sections, sections - current_sections)

                for row in range(current_sections, sections):
                    model.setData(
                        model.index(row, 0),
                        QtCore.QSize(SECTION_WIDTH, self.defaultSectionSize()),
                        QtCore.Qt.ItemDataRole.SizeHintRole,
                    )

    def setSectionLabel(self, section: int, label: str) -> None:
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            index = self.model().index(0, section)
        else:
            index = self.model().index(section, 0)

        self.model().setData(index, label, QtCore.Qt.ItemDataRole.DisplayRole)

    def setSectionBackgroundColor(self, section: int, color: QtGui.QColor) -> None:
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            index = self.model().index(0, section)
        else:
            index = self.model().index(section, 0)

        self.model().setData(index, color, QtCore.Qt.ItemDataRole.BackgroundRole)

    def setSectionForegroundColor(self, section: int, color: QtGui.QColor) -> None:
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            index = self.model().index(0, section)
        else:
            index = self.model().index(section, 0)

        self.model().setData(index, color, QtCore.Qt.ItemDataRole.ForegroundRole)

    def indexAt(self, pos: QtCore.QPoint) -> QtCore.QModelIndex:
        tbl_model = self.model()
        if tbl_model is None:
            return core.ModelIndex()
        if tbl_model.columnCount() == 0 or tbl_model.rowCount() == 0:
            return QtCore.QModelIndex()

        logical_idx = self.logicalIndexAt(pos)
        delta = 0

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            cell_index = tbl_model.index(0, logical_idx)

            if cell_index.isValid():
                cell_size: QtCore.QSize = cell_index.data(
                    QtCore.Qt.ItemDataRole.SizeHintRole
                )
                delta += cell_size.height()

                if pos.y() <= delta:
                    return cell_index

        else:
            cell_index = tbl_model.index(logical_idx, 0)

            if cell_index.isValid():
                cell_size: QtCore.QSize = cell_index.data(
                    QtCore.Qt.ItemDataRole.SizeHintRole
                )
                delta += cell_size.width()

                if pos.x() <= delta:
                    return cell_index

        return QtCore.QModelIndex()

    def paintSection(
        self, painter: QtGui.QPainter, rect: QtCore.QRect, logical_index: int
    ) -> None:
        tbl_model: SpanHeaderModel = self.model()

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            cell_index = tbl_model.index(0, logical_index)
        else:
            cell_index = tbl_model.index(logical_index, 0)

        cell_size: QtCore.QSize = cell_index.data(QtCore.Qt.ItemDataRole.SizeHintRole)
        section_rect = QtCore.QRect(rect)

        section_rect.setSize(cell_size)

        # check up span column or row
        col_span_idx = self.column_span_index(cell_index)
        row_span_idx = self.row_span_index(cell_index)

        if col_span_idx.isValid():
            col_span_from = col_span_idx.column()
            col_span_cnt: int = col_span_idx.data(
                SpanHeaderModel.HeaderRole.ColumnSpanRole
            )
            col_span = self.columnSpanSize(col_span_from, col_span_cnt)

            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                section_rect.setLeft(self.sectionViewportPosition(col_span_from))
            else:
                section_rect.setLeft(self.columnSpanSize(0, col_span_from))

            section_rect.setWidth(col_span)

            cell_index = col_span_idx

        if row_span_idx.isValid():
            row_span_from = row_span_idx.row()
            row_span_cnt: int = row_span_idx.data(SpanHeaderModel.HeaderRole.RowSpanRole)
            row_span = self.rowSpanSize(row_span_from, row_span_cnt)

            if self.orientation() == QtCore.Qt.Orientation.Vertical:
                section_rect.setTop(self.sectionViewportPosition(row_span_from))
            else:
                section_rect.setTop(self.rowSpanSize(0, row_span_from))

            section_rect.setHeight(row_span)

            cell_index = row_span_idx

        # draw section with style
        opt = QtWidgets.QStyleOptionHeader()
        self.initStyleOption(opt)
        opt.textAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        opt.iconAlignment = QtCore.Qt.AlignmentFlag.AlignVCenter
        opt.section = logical_index
        opt.text = cell_index.data(QtCore.Qt.ItemDataRole.DisplayRole)
        opt.rect = section_rect

        bg = cell_index.data(QtCore.Qt.ItemDataRole.BackgroundRole)
        fg = cell_index.data(QtCore.Qt.ItemDataRole.ForegroundRole)
        if bg is not None:
            opt.palette.setBrush(QtGui.QPalette.ColorRole.Button, QtGui.QBrush(bg))
            opt.palette.setBrush(QtGui.QPalette.ColorRole.Window, QtGui.QBrush(bg))
        if fg is not None:
            opt.palette.setBrush(QtGui.QPalette.ColorRole.ButtonText, QtGui.QBrush(fg))

        painter.save()
        self.style().drawControl(
            QtWidgets.QStyle.ControlElement.CE_Header, opt, painter, self
        )
        painter.restore()

    def sectionSizeFromContents(self, logical_index: int) -> QtCore.QSize:
        tbl_model: SpanHeaderModel = self.model()

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            cell_index = tbl_model.index(0, logical_index)
        else:
            cell_index = tbl_model.index(logical_index, 0)

        size = cell_index.data(QtCore.Qt.ItemDataRole.SizeHintRole)

        if size is None:
            size = super().sectionSizeFromContents(logical_index)

        return size

    def setSpan(self, section: int, span_count: int) -> None:
        md: SpanHeaderModel = self.model()

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            idx = md.index(0, section)
            md.setData(idx, 1, SpanHeaderModel.HeaderRole.RowSpanRole)
            md.setData(idx, span_count, SpanHeaderModel.HeaderRole.ColumnSpanRole)
        else:
            idx = md.index(section, 0)
            md.setData(idx, span_count, SpanHeaderModel.HeaderRole.RowSpanRole)
            md.setData(idx, 1, SpanHeaderModel.HeaderRole.ColumnSpanRole)

    def column_span_index(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        tbl_model: SpanHeaderModel = self.model()
        cur_row = index.row()
        cur_col = index.column()
        i = cur_col

        while i >= 0:
            span_index = tbl_model.index(cur_row, i)
            span: int = span_index.data(SpanHeaderModel.HeaderRole.ColumnSpanRole)

            if span is not None and span_index.column() + span - 1 >= cur_col:
                return span_index

            i -= 1

        return QtCore.QModelIndex()

    def row_span_index(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        tbl_model: SpanHeaderModel = self.model()
        cur_row = index.row()
        cur_col = index.column()
        i = cur_row

        while i >= 0:
            span_index = tbl_model.index(i, cur_col)
            span: int = span_index.data(SpanHeaderModel.HeaderRole.RowSpanRole)

            if span is not None and span_index.row() + span - 1 >= cur_row:
                return span_index

            i -= 1

        return QtCore.QModelIndex()

    def columnSpanSize(self, from_col: int, span_count: int) -> int:
        tbl_model: SpanHeaderModel = self.model()
        span = 0

        for col in range(from_col, from_col + span_count):
            cell_size: QtCore.QSize = tbl_model.index(0, col).data(
                QtCore.Qt.ItemDataRole.SizeHintRole
            )
            span += cell_size.width()

        return span

    def rowSpanSize(self, from_row: int, span_count: int) -> int:
        tbl_model: SpanHeaderModel = self.model()
        span = 0

        for row in range(from_row, from_row + span_count):
            cell_size: QtCore.QSize = tbl_model.index(row, 0).data(
                QtCore.Qt.ItemDataRole.SizeHintRole
            )
            span += cell_size.height()

        return span

    def getSectionRange(
        self, index: QtCore.QModelIndex, begin_section: int, end_section: int
    ) -> int:
        col_span_idx = self.column_span_index(index)
        row_span_idx = self.row_span_index(index)

        if col_span_idx.isValid():
            col_span_from = col_span_idx.column()
            col_span_cnt: int = col_span_idx.data(
                SpanHeaderModel.HeaderRole.ColumnSpanRole
            )
            col_span_to = col_span_from + col_span_cnt - 1

            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                begin_section = col_span_from
                end_section = col_span_to
            else:
                sub_row_span_data = col_span_idx.data(
                    SpanHeaderModel.HeaderRole.RowSpanRole
                )

                if sub_row_span_data is not None:
                    subrow_span_from = col_span_idx.row()
                    subrow_span_cnt: int = sub_row_span_data
                    subrow_span_to = subrow_span_from + subrow_span_cnt - 1
                    begin_section = subrow_span_from
                    end_section = subrow_span_to

        elif row_span_idx.isValid():
            row_span_from = row_span_idx.row()
            row_span_cnt: int = row_span_idx.data(SpanHeaderModel.HeaderRole.RowSpanRole)
            row_span_to = row_span_from + row_span_cnt - 1

            if self.orientation() == QtCore.Qt.Orientation.Vertical:
                begin_section = row_span_from
                end_section = row_span_to
            else:
                subcol_span_data = row_span_idx.data(
                    SpanHeaderModel.HeaderRole.ColumnSpanRole
                )

                if subcol_span_data is not None:
                    subcol_span_from = row_span_idx.column()
                    subcol_span_cnt: int = subcol_span_data
                    subcol_span_to = subcol_span_from + subcol_span_cnt - 1

                    begin_section = subcol_span_from
                    end_section = subcol_span_to

        return begin_section, end_section

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

        index = self.indexAt(event.position().toPoint())

        if index.isValid():
            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                begin_section = index.column()
            else:
                begin_section = index.row()

            begin_section, end_section = self.getSectionRange(
                index, begin_section, begin_section
            )

            self.sectionPressed.emit(begin_section, end_section)

    @core.Slot(int, int, int)
    def onSectionResized(self, logical_index: int, old_size: int, new_size: int) -> None:
        tbl_model: SpanHeaderModel = self.model()

        pos = self.sectionViewportPosition(logical_index)

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            xx, yy = pos, 0
            cell_index = tbl_model.index(0, logical_index)
        else:
            xx, yy = 0, pos
            cell_index = tbl_model.index(logical_index, 0)

        section_rect = QtCore.QRect(xx, yy, 0, 0)
        cell_size: QtCore.QSize = cell_index.data(QtCore.Qt.ItemDataRole.SizeHintRole)

        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            cell_size.setWidth(new_size)
        else:
            cell_size.setHeight(new_size)

        tbl_model.setData(cell_index, cell_size, QtCore.Qt.ItemDataRole.SizeHintRole)

        col_span_idx = self.column_span_index(cell_index)
        row_span_idx = self.row_span_index(cell_index)

        if col_span_idx.isValid():
            col_span_from = col_span_idx.column()

            if self.orientation() == QtCore.Qt.Orientation.Horizontal:
                section_rect.setLeft(self.sectionViewportPosition(col_span_from))
            else:
                section_rect.setLeft(self.columnSpanSize(0, col_span_from))

        if row_span_idx.isValid():
            row_span_from = row_span_idx.row()

            if self.orientation() == QtCore.Qt.Orientation.Vertical:
                section_rect.setTop(self.sectionViewportPosition(row_span_from))
            else:
                section_rect.setTop(self.rowSpanSize(0, row_span_from))

        rect_to_update = QtCore.QRect(section_rect)
        rect_to_update.setWidth(self.viewport().width() - section_rect.left())
        rect_to_update.setHeight(self.viewport().height() - section_rect.top())
        self.viewport().update(rect_to_update.normalized())


class SpanTableView(widgets.TableView):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        hheader = SpanHeaderView(QtCore.Qt.Orientation.Horizontal)
        vheader = SpanHeaderView(QtCore.Qt.Orientation.Vertical)

        self.setHorizontalHeader(hheader)
        self.setVerticalHeader(vheader)

        hheader.sectionPressed.connect(self.onHorizontalHeaderSectionPressed)
        vheader.sectionPressed.connect(self.onVerticalHeaderSectionPressed)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        old_model = self.model()

        if old_model is not None:
            old_model.modelReset.disconnect(self.onModelReset)
            old_model.columnsInserted.disconnect(self.onModelColumnsChanged)
            old_model.columnsRemoved.disconnect(self.onModelColumnsChanged)
            old_model.rowsInserted.disconnect(self.onModelRowsChanged)
            old_model.rowsRemoved.disconnect(self.onModelRowsChanged)

        hheader = self.spanHeaderView(QtCore.Qt.Orientation.Horizontal)
        vheader = self.spanHeaderView(QtCore.Qt.Orientation.Vertical)

        hheader_model = hheader.model()
        vheader_model = vheader.model()

        # `QTableView` also sets the model of both headers to `model`.
        # We don't want that, since `SpanHeaderView` has its own model.
        super().setModel(model)

        hheader.setModel(hheader_model)
        vheader.setModel(vheader_model)

        hheader.setSectionCount(model.columnCount())
        vheader.setSectionCount(model.rowCount())

        model.modelReset.connect(self.onModelReset)
        model.columnsInserted.connect(self.onModelColumnsChanged)
        model.columnsRemoved.connect(self.onModelColumnsChanged)
        model.rowsInserted.connect(self.onModelRowsChanged)
        model.rowsRemoved.connect(self.onModelRowsChanged)

    def spanHeaderView(self, orientation: QtCore.Qt.Orientation) -> SpanHeaderView:
        if orientation == QtCore.Qt.Orientation.Horizontal:
            return self.horizontalHeader()
        else:
            return self.verticalHeader()

    @core.Slot(int, int)
    def onHorizontalHeaderSectionPressed(
        self, begin_section: int, end_section: int
    ) -> None:
        self.clearSelection()
        old_selection_mode = self.selectionMode()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)

        for i in range(begin_section, end_section + 1):
            self.selectColumn(i)

        self.setSelectionMode(old_selection_mode)

    @core.Slot(int, int)
    def onVerticalHeaderSectionPressed(
        self, begin_section: int, end_section: int
    ) -> None:
        self.clearSelection()
        old_selection_mode = self.selectionMode()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)

        for i in range(begin_section, end_section + 1):
            self.selectRow(i)

        self.setSelectionMode(old_selection_mode)

    @core.Slot()
    def onModelReset(self) -> None:
        hheader = self.spanHeaderView(QtCore.Qt.Orientation.Horizontal)
        vheader = self.spanHeaderView(QtCore.Qt.Orientation.Vertical)

        hheader.setSectionCount(self.model().columnCount())
        vheader.setSectionCount(self.model().rowCount())

    @core.Slot()
    def onModelColumnsChanged(self) -> None:
        hheader = self.spanHeaderView(QtCore.Qt.Orientation.Horizontal)
        hheader.setSectionCount(self.model().columnCount())

    @core.Slot()
    def onModelRowsChanged(self) -> None:
        vheader = self.spanHeaderView(QtCore.Qt.Orientation.Vertical)
        vheader.setSectionCount(self.model().rowCount())


if __name__ == "__main__":
    from prettyqt import gui

    a = widgets.app()
    w = widgets.Widget()
    w.setLayout(widgets.VBoxLayout())
    view = SpanTableView()
    w.layout().addWidget(view)

    model = gui.StandardItemModel()
    view.setModel(model)

    for i in range(10):
        items = []

        for j in range(10):
            items.append(gui.StandardItem(f"item({i},{j})"))

        model.appendRow(items)

    # Horizontal header settings.
    hheader = view.spanHeaderView(QtCore.Qt.Orientation.Horizontal)

    hheader.setSpan(0, 1)
    hheader.setSpan(1, 2)
    hheader.setSpan(3, 3)
    hheader.setSpan(6, 4)

    hheader.setSectionLabel(0, "section1")
    hheader.setSectionLabel(1, "section2")
    hheader.setSectionLabel(3, "section3")
    hheader.setSectionLabel(6, "section4")

    hheader.setSectionBackgroundColor(0, QtGui.QColor(QtCore.Qt.GlobalColor.cyan))
    hheader.setSectionForegroundColor(0, QtGui.QColor(QtCore.Qt.GlobalColor.blue))

    # Vertical header settings.
    vheader = view.spanHeaderView(QtCore.Qt.Orientation.Vertical)

    vheader.setSpan(0, 4)
    vheader.setSpan(4, 3)
    vheader.setSpan(7, 2)
    vheader.setSpan(9, 1)

    vheader.setSectionLabel(0, "section1")
    vheader.setSectionLabel(4, "section2")
    vheader.setSectionLabel(7, "section3")
    vheader.setSectionLabel(9, "section4")

    w.resize(800, 600)
    w.show()

    a.exec()