from __future__ import annotations

import os

from prettyqt import widgets
from prettyqt.qt import QtSvg


QtSvg.QSvgWidget.__bases__ = (widgets.Widget,)


class SvgWidget(QtSvg.QSvgWidget):
    def load_file(self, path: str | os.PathLike):
        self.load(os.fspath(path))
