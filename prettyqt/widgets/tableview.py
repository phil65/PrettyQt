from typing import Optional

from qtpy import QtWidgets

from prettyqt import constants, widgets


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

    def sort_by_column(self, column: Optional[int], ascending: bool = True):
        column = -1 if column is None else column
        order = constants.ASCENDING if ascending else constants.DESCENDING
        self.sortByColumn(column, order)


if __name__ == "__main__":
    app = widgets.app()
    widget = TableView()
    widget.set_model(widgets.FileSystemModel())
    widget.show()
    app.main_loop()
