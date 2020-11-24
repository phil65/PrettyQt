from qtpy import QtHelp

from prettyqt import core


QtHelp.QHelpIndexModel.__bases__ = (core.StringListModel,)


class HelpIndexModel(QtHelp.QHelpIndexModel):
    pass
