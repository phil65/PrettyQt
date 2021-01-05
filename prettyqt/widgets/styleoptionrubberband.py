from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionRubberBand.__bases__ = (widgets.StyleOption,)


class StyleOptionRubberBand(QtWidgets.QStyleOptionRubberBand):
    pass
