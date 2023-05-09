from __future__ import annotations

from prettyqt import custom_models, widgets
from prettyqt.qt import QtCore


class SubsequenceCompleter(widgets.Completer):
    """QCompleter specialised for subsequence matching."""

    def __init__(self, *args):
        super().__init__(*args)
        self.local_completion_prefix = ""
        self.source_model = None
        self.proxy_model = custom_models.SubsequenceSortFilterProxyModel(parent=self)
        self.proxy_model.setFilterCaseSensitivity(self.caseSensitivity())
        self.proxy_model.set_sort_role("user")
        self._force_next_update = True

    def setModel(self, model: QtCore.QAbstractItemModel):
        self.source_model = model
        self.proxy_model = custom_models.SubsequenceSortFilterProxyModel(parent=self)
        self.proxy_model.setFilterCaseSensitivity(self.caseSensitivity())
        self.proxy_model.set_sort_role("user")
        self.proxy_model.set_prefix(self.local_completion_prefix)
        self.proxy_model.setSourceModel(self.source_model)
        super().setModel(self.proxy_model)
        self.proxy_model.invalidate()
        self.proxy_model.sort(0)
        self._force_next_update = True

    def __getattr__(self, key):
        return getattr(self.proxy_model, key)

    def update_model(self):
        count = self.completionCount()
        if count or len(self.local_completion_prefix) <= 1 or self._force_next_update:
            self.proxy_model.set_prefix(self.local_completion_prefix)
            self.proxy_model.invalidate()  # force sorting/filtering
        if count > 1:
            self.proxy_model.sort(0)
        self._force_next_update = False

    def splitPath(self, path: str) -> list[str]:
        self.local_completion_prefix = path
        self.update_model()
        return [""]


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            a=2,
            b={
                "a": 4,
                "b": [1, 2, 3],
                "jkjkjk": "tekjk",
                "sggg": "tekjk",
                "fdfdf": "tekjk",
                "xxxx": "xxx",
            },
        ),
        6,
        "jkjk",
    ]
    source_model = JsonModel(dist)
    app = widgets.app()
    completer = SubsequenceCompleter()
    completer.setModel(source_model)
    completer.setFilterKeyColumn(1)
    widget = widgets.LineEdit()
    widget.set_completer(completer)
    widget.show()
    app.main_loop()
