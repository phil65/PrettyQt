from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionSpinBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSpinBox(QtWidgets.QStyleOptionSpinBox):
    pass
