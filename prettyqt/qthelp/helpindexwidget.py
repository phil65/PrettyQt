from qtpy import QtHelp

from prettyqt import widgets


QtHelp.QHelpIndexWidget.__bases__ = (widgets.ListView,)


class HelpIndexWidget(QtHelp.QHelpIndexWidget):
    pass
