from prettyqt import widgets
from prettyqt.qt import QtWidgets


QtWidgets.QStyleOptionFocusRect.__bases__ = (widgets.StyleOption,)


class StyleOptionFocusRect(QtWidgets.QStyleOptionFocusRect):
    pass
