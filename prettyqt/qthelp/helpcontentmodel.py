from qtpy import QtHelp

from prettyqt import core


QtHelp.QHelpContentModel.__bases__ = (core.AbstractItemModel,)


class HelpContentModel(QtHelp.QHelpContentModel):
    pass
