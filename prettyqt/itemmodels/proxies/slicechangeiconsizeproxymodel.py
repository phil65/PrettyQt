from __future__ import annotations

import logging

from prettyqt import constants, core, gui, itemmodels
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class SliceChangeIconSizeProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model which changes the icon size of the Decoration role.

    Supports QColors, QPixmaps and QIcons in DecorationRole.
    """

    ID = "change_icon_size"
    ICON = "mdi.resize"

    def __init__(self, size: datatypes.SizeType, **kwargs):
        super().__init__(**kwargs)
        self._size = datatypes.to_size(size)
        self._cache = {}

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if role == constants.DECORATION_ROLE and self.indexer_contains(index):
            original = super().data(index, role)
            match original:
                case gui.QIcon():
                    hashed = original.cacheKey()
                    if hashed in self._cache:
                        return self._cache[hashed]
                    p = original.pixmap(self._size)
                    self._cache[hashed] = p
                    return p
                case gui.QColor():
                    hashed = original.name()
                    if hashed in self._cache:
                        return self._cache[hashed]
                    p = gui.QPixmap(self._size)
                    p.fill(original)
                    self._cache[hashed] = p
                    return p
                case gui.QPixmap():
                    hashed = original.cacheKey()
                    if hashed in self._cache:
                        return self._cache[hashed]
                    p = original.scaled(self._size)
                    self._cache[hashed] = p
                    return p
        return super().data(index, role)

    def set_icon_size(self, size: core.QSize):
        self._cache = {}
        self._size = size

    def get_icon_size(self) -> core.QSize:
        return self._size

    icon_size = core.Property(
        core.QSize,
        get_icon_size,
        set_icon_size,
        doc="New icon size",
    )


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    tree = widgets.TreeView()
    # tree.setUniformRowHeights(False)
    model = widgets.FileSystemModel()
    tree.set_model(model)
    tree.show()
    tree.set_sorting_enabled(True)
    tree.resize(650, 400)
    tree.set_icon("mdi.file-cabinet")
    tree.setWindowTitle("Example")
    index = model.setRootPath("E:/")
    # tree.setRootIndex(index)
    tree.h_header.resize_sections("stretch")
    # tree.proxifier.get_proxy("change_icon_size", size=(30, 30), indexer=None)

    with app.debug_mode():
        app.exec()
