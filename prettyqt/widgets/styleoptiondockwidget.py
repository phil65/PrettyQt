from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionDockWidget.__bases__ = (widgets.StyleOption,)


class StyleOptionDockWidget(QtWidgets.QStyleOptionDockWidget):
    pass
