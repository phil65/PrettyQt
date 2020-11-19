from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionTitleBar.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionTitleBar(QtWidgets.QStyleOptionTitleBar):
    pass
