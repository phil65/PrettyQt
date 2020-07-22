# -*- coding: utf-8 -*-
"""
"""

import pathlib
from typing import Union, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets


class Image(widgets.Label):
    def __init__(
        self,
        path: Union[pathlib.Path, str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(parent=parent)
        if path:
            self.set_image(path)

    def __repr__(self):
        return f"Image({self.text()!r})"

    def __getstate__(self):
        return dict(
            text=self.text(),
            scaled_contents=self.hasScaledContents(),
            margin=self.margin(),
            alignment=int(self.alignment()),
        )

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setMargin(state.get("margin", 0))
        self.setAlignment(QtCore.Qt.Alignment(state.get("alignment")))
        self.setScaledContents(state["scaled_contents"])

    def set_image(self, path: Union[pathlib.Path, str], width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText(
            "<html><head/><body><p>"
            f"<img src={str(path)!r} width={str(width)!r}/>"
            "</p></body></html>"
        )

    @classmethod
    def from_path(cls, path: Union[pathlib.Path, str], parent=None) -> "Image":
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


if __name__ == "__main__":
    app = widgets.app()
    widget = Image("https://act-crm-addon.de/wp-content/uploads/2018/12/test.png")
    widget.show()
    app.exec_()
