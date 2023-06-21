from __future__ import annotations

import logging

from prettyqt import custom_models, constants, core
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)


class SliceChangeIconSizeProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "change_icon_size"

    def __init__(self, size: core.QSize, **kwargs):
        super().__init__(**kwargs)
        self._size = datatypes.to_size(size)
        self._cache = dict()

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.DECORATION_ROLE and self.indexer_contains(index):
            original = super().data(index, role)
            if original is not None:
                hashed = hash(original)
                if hashed in self._cache:
                    return self._cache[hashed]
                else:
                    p = original.pixmap(self._size)
                    self._cache[hashed] = p
                    return p
        return super().data(index, role)

    def set_icon_size(self, size: core.QSize):
        self._size = size

    def get_icon_size(self) -> core.QSize:
        return self._size

    icon_size = core.Property(core.QSize, get_icon_size, set_icon_size)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    tree = widgets.TreeView()
    # tree.setUniformRowHeights(False)
    model = widgets.FileSystemModel(parent=tree)
    model.setRootPath("C:/")
    tree.set_model(model)
    tree.proxifier.get_proxy(
        "change_icon_size", size=(100, 100), indexer=(None, slice(None, None, 2))
    )
    tree.show()
    with app.debug_mode():
        app.exec()
