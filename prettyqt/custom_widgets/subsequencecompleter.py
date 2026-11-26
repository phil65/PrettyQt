from prettyqt import constants, core, widgets


class SubsequenceProxyModel(core.SortFilterProxyModel):
    """Accepts rows whose text contains the search term's characters in order."""

    def set_search_term(self, search_term: str):
        self.setFilterString(search_term)


class SubsequenceCompleter(widgets.Completer):
    """QCompleter specialised for subsequence matching."""

    def __init__(self, *args):
        super().__init__(*args)
        self.completion_search_term = ""
        self.source_model = None
        self.set_completion_mode("unfiltered_popup")
        self.proxy_model = SubsequenceProxyModel(parent=self)
        self.proxy_model.setFilterCaseSensitivity(self.caseSensitivity())
        self.set_case_sensitive(False)
        self._force_next_update = True
        self.path_updated.connect(self._on_path_updated)
        self.setCompletionRole(constants.DISPLAY_ROLE)

    def setModel(self, model: core.QAbstractItemModel):
        self.source_model = model
        self.proxy_model = SubsequenceProxyModel(parent=self)
        self.proxy_model.setFilterCaseSensitivity(self.caseSensitivity())
        self.proxy_model.set_search_term(self.completion_search_term)
        self.proxy_model.setSourceModel(self.source_model)
        super().setModel(self.proxy_model)
        self.proxy_model.invalidateRowsFilter()
        # self.proxy_model.sort(0)
        self._force_next_update = True

    # def __getattr__(self, key):
    #     return getattr(self.proxy_model, key)

    def set_case_sensitive(self, value: bool):
        super().set_case_sensitive(value)
        self.proxy_model.set_filter_case_sensitive(value)

    def _on_path_updated(self, path: str):
        if path == self.completion_search_term:
            return
        self.completion_search_term = path
        count = self.completionCount()
        if count or len(self.completion_search_term) <= 1 or self._force_next_update:
            self.proxy_model.set_search_term(self.completion_search_term)
        if count > 1:
            self.proxy_model.sort(0)
        self._force_next_update = False
        self.proxy_model.invalidateRowsFilter()  # force sorting/filtering


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.itemmodels.importlibdistributionmodel import (
        ImportlibTreeModel,
    )

    app = widgets.app()
    source_model = ImportlibTreeModel.from_package("prettyqt")
    completer = SubsequenceCompleter()
    completer.setModel(source_model)

    lineedit = widgets.LineEdit()
    lineedit.set_completer(completer)
    widget = widgets.Widget()
    widget.set_layout("vertical")
    widget.box.add(lineedit)
    table = widgets.TableView()
    widget.box.add(table)
    table.set_model(source_model)
    widget.show()
    app.exec()
