from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionGroupBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionGroupBox(QtWidgets.QStyleOptionGroupBox):
    pass
