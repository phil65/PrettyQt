from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QDesktopWidget.__bases__ = (widgets.Widget,)


class DesktopWidget(QtWidgets.QDesktopWidget):
    pass
