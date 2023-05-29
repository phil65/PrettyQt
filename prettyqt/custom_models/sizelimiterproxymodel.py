from __future__ import annotations

from prettyqt import core


class SizeLimiterProxyModel(core.IdentityProxyModel):
    ID = "size_limiter"

    def __init__(self, size: tuple[int | None, int | None] | None = None, **kwargs):
        self._row_count = None
        self._col_count = None
        super().__init__(**kwargs)
        self.set_size(size)

    def rowCount(self, index=None):
        rowcount = super().rowCount()
        return min(rowcount, self._row_count) if self._row_count is not None else rowcount

    def columnCount(self, index=None):
        colcount = super().columnCount()
        return min(colcount, self._col_count) if self._col_count is not None else colcount

    def set_size(self, size: tuple[int | None, int | None] | None):
        if size is None:
            size = (None, None)
        self._row_count, self._col_count = size


if __name__ == "__main__":
    from prettyqt import widgets
    from prettyqt.custom_models import JsonModel

    app = widgets.app()
    dist = [
        dict(
            assss=2,
            bffff={
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

    table = widgets.TreeView()
    _source_model = JsonModel(dist, parent=table)
    model = SizeLimiterProxyModel(parent=table, size=(1, 1))
    model.setSourceModel(_source_model)
    table.setRootIsDecorated(True)
    table.set_model(model)
    table.show()
    with app.debug_mode():
        app.main_loop()
