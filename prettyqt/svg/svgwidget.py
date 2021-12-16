from __future__ import annotations

import os

from prettyqt import widgets
from prettyqt.qt import QtSvg
from prettyqt.utils import types


QtSvg.QSvgWidget.__bases__ = (widgets.Widget,)


class SvgWidget(QtSvg.QSvgWidget):
    def load_file(self, path: types.PathType):
        self.load(os.fspath(path))
