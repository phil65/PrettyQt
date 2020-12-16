from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionComplex.__bases__ = (widgets.StyleOption,)


class StyleOptionComplex(QtWidgets.QStyleOptionComplex):
    pass
