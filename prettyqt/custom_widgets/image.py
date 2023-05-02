from __future__ import annotations

import os

from typing_extensions import Self

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import datatypes, get_repr


class Image(widgets.Label):
    def __init__(
        self,
        path: datatypes.PathType | None = None,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        if path:
            self.set_image(path)

    def __repr__(self):
        return get_repr(self)

    def set_image(self, path: datatypes.PathType, width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText(
            "<html><head/><body><p>"
            f"<img src={os.fspath(path)!r} width={str(width)!r}/>"
            "</p></body></html>"
        )

    @classmethod
    def from_path(
        cls, path: datatypes.PathType, parent: QtWidgets.QWidget | None = None
    ) -> Self:
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
