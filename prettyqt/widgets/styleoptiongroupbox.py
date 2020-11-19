from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionGroupBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionGroupBox(QtWidgets.QStyleOptionGroupBox):
    pass
