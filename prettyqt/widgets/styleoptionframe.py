from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionFrame.__bases__ = (widgets.StyleOption,)


class StyleOptionFrame(QtWidgets.QStyleOptionFrame):
    pass
