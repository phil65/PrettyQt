from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionToolButton.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionToolButton(QtWidgets.QStyleOptionToolButton):
    pass
