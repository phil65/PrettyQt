from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionProgressBar.__bases__ = (widgets.StyleOption,)


class StyleOptionProgressBar(QtWidgets.QStyleOptionProgressBar):
    pass
