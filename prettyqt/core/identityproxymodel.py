from qtpy import QtCore

from prettyqt import core


QtCore.QIdentityProxyModel.__bases__ = (core.AbstractProxyModel,)


class IdentityProxyModel(QtCore.QIdentityProxyModel):
    pass
