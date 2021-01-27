from __future__ import annotations

import os
from typing import Union

from prettyqt import widgets
from prettyqt.qt import QtSvg


QtSvg.QSvgWidget.__bases__ = (widgets.Widget,)


class SvgWidget(QtSvg.QSvgWidget):
    def load_file(self, path: Union[str, os.PathLike]):
        self.load(os.fspath(path))
