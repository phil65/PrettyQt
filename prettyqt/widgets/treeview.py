from __future__ import annotations

from collections.abc import Iterable
from prettyqt import constants, core, widgets


class TreeViewMixin(widgets.AbstractItemViewMixin):
    def __init__(
        self,
        *args,
        root_is_decorated: bool = True,
        all_columns_show_focus: bool = True,
        uniform_row_heights: bool = True,
        alternating_row_colors: bool = True,
        selection_mode: str = "extended",
        **kwargs,
    ):
        super().__init__(
            *args,
            root_is_decorated=root_is_decorated,
            all_columns_show_focus=all_columns_show_focus,
            uniform_row_heights=uniform_row_heights,
            alternating_row_colors=alternating_row_colors,
            selection_mode=selection_mode,
            **kwargs,
        )
        class_name = type(self).__name__
        self.set_id(class_name)
        # misc
        self.h_header = widgets.HeaderView("horizontal", parent=self)

    @property
    def h_header(self):
        return self.header()

    @h_header.setter
    def h_header(self, header):
        self.setHeader(header)

    def show_root(self, value: bool):
        self.setRootIndex(core.QModelIndex())
        if not value:
            self.setRootIndex(self.model().index(0, 0))

    def set_expanded(
        self, index: core.ModelIndex | Iterable[core.ModelIndex], expanded: bool = True
    ):
        """Set expaned state of an index or an Iterable of indexes."""
        match index:
            case Iterable():
                for idx in index:
                    self.setExpanded(idx, expanded)
            case _:
                self.setExpanded(index, expanded)

    def set_sorting_enabled(self, enabled: bool, do_sort: bool = False):
        """Hack to avoid direct sort when setting sorting enabled."""
        model = self.model()
        if not do_sort and model is not None:
            backup = model.sort
            model.sort = lambda x, y: None
        self.setSortingEnabled(enabled)
        if not do_sort and model is not None:
            model.sort = backup

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


class TreeView(TreeViewMixin, widgets.QTreeView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    dlg = widgets.MainWindow()
    status_bar = TreeView()
    dlg.show()
    app.exec()
