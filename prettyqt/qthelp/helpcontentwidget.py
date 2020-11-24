from qtpy import QtHelp

from prettyqt import widgets


QtHelp.QHelpContentWidget.__bases__ = (widgets.TreeView,)


class HelpContentWidget(QtHelp.QHelpContentWidget):
    pass
