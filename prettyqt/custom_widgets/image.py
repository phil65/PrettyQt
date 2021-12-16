from __future__ import annotations

import os

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import types


class Image(widgets.Label):
    def __init__(
        self,
        path: types.PathType | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        if path:
            self.set_image(path)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def set_image(self, path: types.PathType, width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText(
            "<html><head/><body><p>"
            f"<img src={os.fspath(path)!r} width={str(width)!r}/>"
            "</p></body></html>"
        )

    @classmethod
    def from_path(
        cls, path: types.PathType, parent: QtWidgets.QWidget | None = None
    ) -> Image:
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


if __name__ == "__main__":
    app = widgets.app()
    widget = Image("https://act-crm-addon.de/wp-content/uploads/2018/12/test.png")
    widget.show()
    bool(widget)
    app.main_loop()
