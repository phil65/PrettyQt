from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionSizeGrip.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSizeGrip(QtWidgets.QStyleOptionSizeGrip):
    pass
