from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionComboBox.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionComboBox(QtWidgets.QStyleOptionComboBox):
    pass
