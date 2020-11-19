from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionSizeGrip.__bases__ = (widgets.StyleOptionComplex,)


class StyleOptionSizeGrip(QtWidgets.QStyleOptionSizeGrip):
    pass
