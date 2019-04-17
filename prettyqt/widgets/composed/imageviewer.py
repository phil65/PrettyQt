# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from prettyqt import widgets


class ImageViewer(widgets.Widget):

    def __init__(self, title="", path=None, parent=None):
        super().__init__(parent)
        if title:
            self.setWindowTitle(title)
        self.image = None
        if path:
            self.image = widgets.Label.image_from_path(path, parent=self)
        self.show()


if __name__ == "__main__":
    app = widgets.Application(sys.argv)
    ex = ImageViewer()
    sys.exit(app.exec_())
