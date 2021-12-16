from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


class ImageViewer(widgets.Widget):
    def __init__(
        self,
        title: str = "",
        path: types.PathType | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent)
        if title:
            self.set_title(title)
        self.image = None
        if path:
            self.image = widgets.Label.image_from_path(path, parent=self)
        self.show()


if __name__ == "__main__":
    app = widgets.app()
    ex = ImageViewer()
    app.main_loop()
