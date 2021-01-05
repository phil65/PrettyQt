from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionTabWidgetFrame.__bases__ = (widgets.StyleOption,)


class StyleOptionTabWidgetFrame(QtWidgets.QStyleOptionTabWidgetFrame):
    pass
