from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class AbstractProxyModelMixin(core.AbstractItemModelMixin):
    def first_item_index(self) -> core.ModelIndex:
        """Return the first child of the root item."""
        # We cannot just call the same function of the source model because the first node
        # there may be hidden.
        proxy_root_index = self.mapFromSource(core.ModelIndex())
        return self.index(0, 0, proxy_root_index)


class AbstractProxyModel(AbstractProxyModelMixin, QtCore.QAbstractProxyModel):
    pass
