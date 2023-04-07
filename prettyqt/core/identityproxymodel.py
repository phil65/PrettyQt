from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class IdentityProxyModel(core.AbstractProxyModelMixin, QtCore.QIdentityProxyModel):
    pass
