from __future__ import annotations

from prettyqt import constants, core, itemmodels, widgets


class FuzzyCompleter(widgets.Completer):
    def __init__(self, parent):
        super().__init__(parent)
        parent.setEditable(True)
        parent.set_insert_policy("no_insert")
        parent.installEventFilter(self)
        self.set_completion_mode("popup")
        self._local_completion_prefix = ""
        self._source_model = None
        self._filter_proxy = itemmodels.FuzzyFilterProxyModel(self)
        self._filter_proxy.set_match_color(None)
        self._using_original_model = False

    def setModel(self, model):
        self._source_model = model
        self._filter_proxy = itemmodels.FuzzyFilterProxyModel(self)
        self._filter_proxy.set_match_color(None)
        self._filter_proxy.setSourceModel(self._source_model)
        super().setModel(self._filter_proxy)
        self._using_original_model = True

    def eventFilter(self, source: widgets.QLineEdit, event: core.QEvent) -> bool:
        match event.type():
            case core.QEvent.Type.FocusIn:
                source.clearEditText()
            case core.QEvent.Type.KeyPress:
                key = event.key()
                if key == constants.Key.Key_Enter:
                    text = source.currentText()
                    source.setCompleter(None)
                    source.setEditText(text)
                    source.setCompleter(source.comp)
        return super().eventFilter(source, event)

    def updateModel(self):
        if not self._using_original_model:
            self._filter_proxy.setSourceModel(self._source_model)

        self._filter_proxy.set_search_term(self._local_completion_prefix)

    def splitPath(self, path):
        self._local_completion_prefix = path
        self.updateModel()
        if self._filter_proxy.rowCount() == 0:
            self._using_original_model = False
            model = core.StringListModel([path])
            self._filter_proxy.setSourceModel(model)
            return [path]

        return []


if __name__ == "__main__":
    from prettyqt import custom_widgets

    app = widgets.app()
    widget = custom_widgets.StandardIconsWidget()
    widget.show()
    app.exec()
