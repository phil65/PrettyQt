# -*- coding: utf-8 -*-
"""
"""

from typing import Optional, Union
import pathlib

from qtpy import QtWidgets

from prettyqt import widgets


class ImageViewer(widgets.Widget):
    def __init__(
        self,
        title: str = "",
        path: Union[pathlib.Path, str] = None,
        parent: Optional[QtWidgets.QWidget] = None,
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
    app.exec_()
