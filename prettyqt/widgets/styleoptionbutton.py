from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionButton.__bases__ = (widgets.StyleOption,)


class StyleOptionButton(QtWidgets.QStyleOptionButton):
    pass
