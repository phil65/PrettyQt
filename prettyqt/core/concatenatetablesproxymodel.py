from qtpy import QtCore

from prettyqt import core


QtCore.QConcatenateTablesProxyModel.__bases__ = (core.AbstractItemModel,)


class ConcatenateTablesProxyModel(QtCore.QConcatenateTablesProxyModel):

    pass
