from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionSpinBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSpinBox(QtWidgets.QStyleOptionSpinBox):
    pass
