from __future__ import annotations

import logging

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets

logger = logging.getLogger(__name__)


class TableViewMixin(widgets.AbstractItemViewMixin):
    def __init__(
        self,
        *args,
        alternating_row_colors: bool = True,
        word_wrap: bool = False,
        **kwargs,
    ):
        super().__init__(
            *args,
            alternating_row_colors=alternating_row_colors,
            word_wrap=word_wrap,
            **kwargs,
        )
        class_name = type(self).__name__
        self.setObjectName(class_name)
        self.setHorizontalHeader(widgets.HeaderView("horizontal", parent=self))
        self.setVerticalHeader(widgets.HeaderView("vertical", parent=self))
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"gridStyle": constants.PEN_STYLE}
        return maps

    @property
    def h_header(self):
        return self.horizontalHeader()

    @h_header.setter
    def h_header(self, header):
        self.setHorizontalHeader(header)

    @property
    def v_header(self):
        return self.verticalHeader()

    @v_header.setter
    def v_header(self, header):
        self.setVerticalHeader(header)

    def is_cell_visible(self, row: int, column: int) -> bool:
        is_in_horizontal = self.h_header.is_in_visual_range(column)
        is_in_vertical = self.v_header.is_in_visual_range(row)
        return is_in_horizontal and is_in_vertical

    def set_sorting_enabled(self, enabled: bool, do_sort: bool = False):
        """Hack to avoid direct sort when setting sorting enabled."""
        model = self.model()
        if not do_sort and model is not None:
            backup = model.sort
            model.sort = lambda x, y: None
        self.setSortingEnabled(enabled)
        if not do_sort and model is not None:
            model.sort = backup

    def setup_list_style(self):
        self.set_selection_behavior("rows")
        self.h_header.setStretchLastSection(True)
        self.v_header.set_resize_mode("fixed")
        self.v_header.set_default_section_size(28)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.resizeColumnsToContents()
        else:
            self.h_header.resize_sections("interactive")

    def sort_by_column(self, column: int | None, ascending: bool = True):
        column = -1 if column is None else column
        order = constants.ASCENDING if ascending else constants.DESCENDING
        self.sortByColumn(column, order)

    def set_grid_style(self, style: constants.PenStyleStr | constants.PenStyle):
        """Set grid style.

        Args:
            style: grid style to use
        """
        self.setGridStyle(constants.PEN_STYLE.get_enum_value(style))

    def get_grid_style(self) -> constants.PenStyleStr:
        """Return grid style.

        Returns:
            grid style
        """
        return constants.PEN_STYLE.inverse[self.gridStyle()]

    def get_visible_section_span(
        self,
        orientation: constants.OrientationStr | constants.Orientation,
        margin: int = 0,
    ) -> tuple[int, int]:
        """Get a tuple containing the visible start/end indexes.

        if there are no items visible, return -1, -1
        """
        rect = self.viewport().rect()
        if orientation in ["horizontal", constants.HORIZONTAL]:
            start = self.columnAt(rect.left())
            count = self.model().columnCount()
            end = self.columnAt(rect.right())
        else:
            start = self.rowAt(rect.top())
            count = self.model().rowCount()
            end = self.rowAt(rect.bottom())
        if count == 0:
            return (-1, -1)
        start = max(0, start - margin)
        end = count if end == -1 else min(end + margin, count)
        return (start, end)

    def resizeColumnsToContents(self, max_columns: int | None = 500):
        colcount = self.model().columnCount()
        if max_columns is None or colcount > max_columns:
            super().resizeColumnsToContents()
            return
        to_check = min(colcount, max_columns)
        for i in range(to_check):
            self.resizeColumnToContents(i)

    def resize_visible_columns_to_contents(self, margin: int = 0):
        if not self.isVisible():
            logger.warning("trying resize_visible_columns_to_contents while not visible.")
        colcount = self.model().columnCount()
        autosized_cols = set()
        col, end = self.get_visible_section_span("horizontal", margin=margin)
        width = self.viewport().width()
        while col <= end:
            if col not in autosized_cols:
                autosized_cols.add(col)
                self.resizeColumnToContents(col)
            col += 1
            #  end may change during resize
            end = self.columnAt(width)
            end = colcount if end == -1 else end

    def auto_span(
        self,
        orientation: constants.OrientationStr
        | constants.Orientation = constants.HORIZONTAL,
        role=constants.DISPLAY_ROLE,
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] | None = None,
    ) -> list[tuple[int, int, int, int]]:
        """Set spans in given direction based on same content in given role."""
        is_horizontal = orientation in [constants.HORIZONTAL, "horizontal"]
        model = self.model()
        spans = []
        # figure out the ranges
        if is_horizontal:
            start_level = max(0, start[0])
            start_section = max(0, start[1])
            end_level = model.rowCount()
            end_section = model.columnCount()
            if end:
                end_level = min(max(0, end[0]), end_level)
                end_section = min(max(0, end[1]), end_section)
        else:
            start_level = max(0, start[1])
            start_section = max(0, start[0])
            end_level = model.columnCount()
            end_section = model.rowCount()
            if end:
                end_level = min(max(0, end[1]), end_level)
                end_section = min(max(0, end[0]), end_section)

        # adjust the spans.
        for level in range(start_level, end_level):
            match_start = None
            if is_horizontal:
                arr = [
                    model.index(level, i).data(role)
                    for i in range(start_section, end_section + 1)
                ]
                logger.debug(f"{type(self).__name__}: spanning horizontal {arr}")
            else:
                arr = [
                    model.index(i, level).data(role)
                    for i in range(start_section, end_section + 1)
                ]
                logger.debug(f"{type(self).__name__}: spanning vertical {arr}")
            for section in range(1, len(arr)):
                if arr[section] == arr[section - 1]:
                    if match_start is None:
                        match_start = section - 1
                    # If this is the last cell, need to end it
                    if section == end_section - start_section:
                        match_end = section
                        span_size = match_end - match_start + 1
                        begin = match_start + start_section
                        if is_horizontal:
                            self.setSpan(level, begin, 1, span_size)
                            spans.append((level, begin, 1, span_size))
                        else:
                            spans.append((begin, level, span_size, 1))
                            self.setSpan(begin, level, span_size, 1)
                elif match_start is not None:
                    match_end = section - 1
                    span_size = match_end - match_start + 1
                    begin = match_start + start_section
                    if is_horizontal:
                        self.setSpan(level, begin, 1, span_size)
                        spans.append((level, begin, 1, span_size))
                    else:
                        self.setSpan(begin, level, span_size, 1)
                        spans.append((begin, level, span_size, 1))
                    match_start = None
        return spans


class TableView(TableViewMixin, QtWidgets.QTableView):
    pass


if __name__ == "__main__":
    from prettyqt import debugging

    app = widgets.app()
    widget = debugging.example_table()
    widget.set_delegate("variant")
    test = widget.model()[2, :]
    print(test)
    widget.show()
    widget.resize(500, 500)
    widget.resize_visible_columns_to_contents()
    app.exec()
