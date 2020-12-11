from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionFocusRect.__bases__ = (widgets.StyleOption,)


class StyleOptionFocusRect(QtWidgets.QStyleOptionFocusRect):
    pass
