from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QTableView.__bases__ = (widgets.AbstractItemView,)


class TableView(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_name = type(self).__name__
        self.set_id(class_name)
        self.setHorizontalHeader(widgets.HeaderView("horizontal", parent=self))
        self.setVerticalHeader(widgets.HeaderView("vertical", parent=self))
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

    def serialize_fields(self):
        return dict(
            corner_button_enabled=self.isCornerButtonEnabled(),
            grid_style=self.get_grid_style(),
            show_grid=self.showGrid(),
            sorting_enabled=self.isSortingEnabled(),
            word_wrap=self.wordWrap(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setCornerButtonEnabled(state["corner_button_enabled"])
        self.set_grid_style(state["grid_style"])
        self.setShowGrid(state["show_grid"])
        self.setSortingEnabled(state["sorting_enabled"])
        self.setWordWrap(state["word_wrap"])

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

    def setup_list_style(self):
        self.set_selection_behaviour("rows")
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


if __name__ == "__main__":
    app = widgets.app()
    widget = TableView()
    widget.set_model(widgets.FileSystemModel())
    widget.show()
    app.main_loop()
