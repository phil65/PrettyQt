from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QIdentityProxyModel.__bases__ = (core.AbstractProxyModel,)


class IdentityProxyModel(QtCore.QIdentityProxyModel):
    pass
