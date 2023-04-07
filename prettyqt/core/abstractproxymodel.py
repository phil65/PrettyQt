from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractProxyModelMixin(core.AbstractItemModelMixin):
    pass


class AbstractProxyModel(AbstractProxyModelMixin, QtCore.QAbstractProxyModel):
    pass
