from __future__ import annotations

import os
from typing import Optional, Union

from prettyqt import gui, widgets
from prettyqt.qt import QtWidgets


class Image(widgets.Label):
    def __init__(
        self,
        path: Union[os.PathLike, str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        if path:
            self.set_image(path)

    def __repr__(self):
        return f"{type(self).__name__}()"

    def set_image(self, path: Union[os.PathLike, str], width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText(
            "<html><head/><body><p>"
            f"<img src={os.fspath(path)!r} width={str(width)!r}/>"
            "</p></body></html>"
        )

    @classmethod
    def from_path(
        cls, path: Union[os.PathLike, str], parent: Optional[QtWidgets.QWidget] = None
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
