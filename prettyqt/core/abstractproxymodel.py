from __future__ import annotations

import logging
from typing import Any

from collections.abc import Callable, Generator

from prettyqt import core, qt
from prettyqt.qt import QtCore

logger = logging.getLogger(__name__)


class AbstractProxyModelMixin(core.AbstractItemModelMixin):
    ID = ""

    def __pretty__(
        self, fmt: Callable[[Any], Any], **kwargs: Any
    ) -> Generator[Any, None, None]:
        yield f"{type(self).__name__}("
        yield 1
        # yield 1
        yield f"objectName={self.objectName()}"
        yield 0
        for k, v in self.get_properties(include_super=False).items():
            yield f"{k}={v!r}"
            yield 0
        model = self.sourceModel()
        if hasattr(model, "__pretty__"):
            yield from model.__pretty__(fmt, **kwargs)
            yield 0
        yield -1
        # yield -1
        yield ")"

    def parent(self, *args):
        # workaround: PyQt6 QIdentityproxymodel.parent() missing
        if not args and qt.API == "pyqt6":
            return QtCore.QAbstractProxyModel.parent(self)
        return super().parent(*args)

    def first_item_index(self) -> core.ModelIndex:
        """Return the first child of the root item."""
        # We cannot just call the same function of the source model because the first node
        # there may be hidden.
        proxy_root_index = self.mapFromSource(core.ModelIndex())
        return self.index(0, 0, proxy_root_index)


class AbstractProxyModel(AbstractProxyModelMixin, QtCore.QAbstractProxyModel):
    pass
