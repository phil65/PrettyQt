from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


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

    def serialize_fields(self):
        return dict(
            all_columns_show_focus=self.allColumnsShowFocus(),
            animated=self.isAnimated(),
            auto_expand_delay=self.autoExpandDelay(),
            expands_on_double_click=self.expandsOnDoubleClick(),
            header_hidden=self.isHeaderHidden(),
            indentation=self.indentation(),
            items_expandable=self.itemsExpandable(),
            root_is_decorated=self.rootIsDecorated(),
            sorting_enabled=self.isSortingEnabled(),
            uniform_row_heights=self.uniformRowHeights(),
            word_wrap=self.wordWrap(),
        )

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
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.h_header.setStretchLastSection(True)

    def adapt_sizes(self):
        model = self.model()
        if model is not None and (model.rowCount() * model.columnCount()) < 1000:
            self.h_header.resizeSections(self.h_header.ResizeMode.ResizeToContents)
        else:
            self.h_header.resize_sections("interactive")

    def sort_by_column(self, column: int | None, ascending: bool = True):
        column = -1 if column is None else column
        order = constants.ASCENDING if ascending else constants.DESCENDING
        self.sortByColumn(column, order)


if __name__ == "__main__":
    app = widgets.app()
    dlg = widgets.MainWindow()
    status_bar = TreeView()
    dlg.show()
    app.main_loop()
