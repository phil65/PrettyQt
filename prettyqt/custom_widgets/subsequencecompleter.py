from __future__ import annotations

from prettyqt import constants, custom_models, widgets
from prettyqt.qt import QtCore


class SubsequenceCompleter(widgets.Completer):
    """QCompleter specialised for subsequence matching."""

    def __init__(self, *args):
        super().__init__(*args)
        self.completion_search_term = ""
        self.source_model = None
        self.set_completion_mode("unfiltered_popup")
        self.proxy_model = custom_models.SubsequenceSortFilterProxyModel(parent=self)
        self.proxy_model.setFilterCaseSensitivity(self.caseSensitivity())
        self.set_case_sensitive(False)
        self._force_next_update = True
        self.path_updated.connect(self._on_path_updated)
        self.setCompletionRole(constants.DISPLAY_ROLE)

    def setModel(self, model: QtCore.QAbstractItemModel):
        self.source_model = model
        self.proxy_model = custom_models.SubsequenceSortFilterProxyModel(parent=self)
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
            return None
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
    from prettyqt.custom_models.importlibdistributionmodel import (
        ImportlibDistributionModel,
    )

    app = widgets.app()
    source_model = ImportlibDistributionModel.from_package("prettyqt")
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
    app.main_loop()
