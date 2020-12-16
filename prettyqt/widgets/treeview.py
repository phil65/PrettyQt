from typing import Optional

from qtpy import QtWidgets

from prettyqt import constants, widgets


QtWidgets.QTreeView.__bases__ = (widgets.AbstractItemView,)


class TreeView(QtWidgets.QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_name = type(self).__name__
        self.set_id(class_name)
        # visual settings
        self.setAnimated(True)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)

        # misc
        self.h_header = widgets.HeaderView("horizontal", parent=self)
        self.set_selection_mode("extended")

    @property
    def h_header(self):
        return self.header()

    @h_header.setter
    def h_header(self, header):
        self.setHeader(header)

    def expand_all(self):
        self.expandAll()

    def set_indentation(self, indentation: int):
        self.setIndentation(indentation)

    def setup_list_style(self):
        self.setSelectionBehavior(self.SelectRows)
        self.h_header.setStretchLastSection(True)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.h_header.resizeSections(self.h_header.ResizeToContents)
        else:
            self.h_header.resize_sections("interactive")

    def sort_by_column(self, column: Optional[int], ascending: bool = True):
        column = -1 if column is None else column
        order = constants.ASCENDING if ascending else constants.DESCENDING
        self.sortByColumn(column, order)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = QtWidgets.QMainWindow()
    status_bar = TreeView()
    dlg.show()
    app.main_loop()
