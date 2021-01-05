from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionProgressBar.__bases__ = (widgets.StyleOption,)


class StyleOptionProgressBar(QtWidgets.QStyleOptionProgressBar):
    pass
