from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


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
        self.set_id(class_name)
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
        return self.h_header.is_in_visual_range(
            column
        ) and self.v_header.is_in_visual_range(row)

    def set_sorting_enabled(self, enabled: bool, do_sort: bool = False):
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

    def set_grid_style(self, style: constants.PenStyleStr):
        """Set grid style.

        Args:
            style: grid style to use

        Raises:
            InvalidParamError: invalid grid style
        """
        if style not in constants.PEN_STYLE:
            raise InvalidParamError(style, constants.PEN_STYLE)
        self.setGridStyle(constants.PEN_STYLE[style])

    def get_grid_style(self) -> constants.PenStyleStr:
        """Return grid style.

        Returns:
            grid style
        """
        return constants.PEN_STYLE.inverse[self.gridStyle()]

    def get_visible_section_span(
        self, orientation: constants.OrientationStr
    ) -> tuple[int, int]:
        rect = self.rect()
        if orientation == "horizontal":
            start = self.columnAt(rect.left())
            count = self.model().columnCount()
            end = self.columnAt(rect.right())
        else:
            start = self.rowAt(rect.top())
            count = self.model().rowRount()
            end = self.rowAt(rect.bottom())
        if count == 0:
            return (-1, -1)
        end = count if end == -1 else end + 1
        return (start, end)

    def resizeColumnsToContents(self, max_columns: int | None = 500):
        colcount = self.model().columnCount()
        if max_columns is None or colcount > max_columns:
            super().resizeColumnsToContents()
            return
        to_check = min(colcount, max_columns)
        for i in range(to_check):
            self.resizeColumnToContents(i)

    def auto_span(
        self,
        orientation=constants.HORIZONTAL,
        role=constants.DISPLAY_ROLE,
        max_sections: int = 5000,
    ):
        is_horizontal = orientation == constants.HORIZONTAL
        model = self.model()
        n = model.rowCount() if is_horizontal else model.columnCount()
        n = min(max_sections, n)
        m = model.columnCount() if is_horizontal else model.rowCount()
        m = min(max_sections, n)
        for level in range(n):
            match_start = None
            if is_horizontal:
                arr = [self.model().index(level, i).data(role) for i in range(m)]
            else:
                arr = [self.model().index(i, level).data(role) for i in range(m)]
            for col in range(1, m):
                if arr[col] == arr[col - 1]:
                    if match_start is None:
                        match_start = col - 1
                    # If this is the last cell, need to end it
                    if col == len(arr) - 1:
                        match_end = col
                        span_size = match_end - match_start + 1
                        if is_horizontal:
                            self.setSpan(level, match_start, 1, span_size)
                        else:
                            self.setSpan(match_start, level, span_size, 1)
                elif match_start is not None:
                    match_end = col - 1
                    span_size = match_end - match_start + 1
                    if is_horizontal:
                        self.setSpan(level, match_start, 1, span_size)
                    else:
                        self.setSpan(match_start, level, span_size, 1)
                    match_start = None


class TableView(TableViewMixin, QtWidgets.QTableView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = TableView()
    widget.set_model(widgets.FileSystemModel())
    widget.show()
    app.main_loop()
