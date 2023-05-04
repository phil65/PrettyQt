from __future__ import annotations

import os

from prettyqt import widgets
from prettyqt.qt import QtSvgWidgets
from prettyqt.utils import datatypes


class SvgWidget(widgets.WidgetMixin, QtSvgWidgets.QSvgWidget):
    def load_file(self, path: datatypes.PathType):
        self.load(os.fspath(path))
