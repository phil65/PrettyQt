from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QStyleOptionDockWidget.__bases__ = (widgets.StyleOption,)


class StyleOptionDockWidget(QtWidgets.QStyleOptionDockWidget):
    pass
