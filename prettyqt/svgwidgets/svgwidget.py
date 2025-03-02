from __future__ import annotations

import os
from typing import TYPE_CHECKING

from prettyqt import widgets
from prettyqt.qt import QtSvgWidgets


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class SvgWidget(widgets.WidgetMixin, QtSvgWidgets.QSvgWidget):
    def load_file(self, path: datatypes.PathType):
        self.load(os.fspath(path))
