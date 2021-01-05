from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionComplex.__bases__ = (widgets.StyleOption,)


class StyleOptionComplex(QtWidgets.QStyleOptionComplex):
    pass
