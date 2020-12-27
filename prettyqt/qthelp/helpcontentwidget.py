from prettyqt import widgets
from prettyqt.qt import QtHelp


QtHelp.QHelpContentWidget.__bases__ = (widgets.TreeView,)


class HelpContentWidget(QtHelp.QHelpContentWidget):
    pass
