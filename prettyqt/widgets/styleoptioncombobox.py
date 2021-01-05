from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionComboBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionComboBox(QtWidgets.QStyleOptionComboBox):
    pass
