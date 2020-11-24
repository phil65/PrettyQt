from qtpy import QtHelp

from prettyqt import widgets


QtHelp.QHelpSearchQueryWidget.__bases__ = (widgets.Widget,)


class HelpSearchQueryWidget(QtHelp.QHelpSearchQueryWidget):
    pass
