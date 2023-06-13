from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class StringListModelMixin(core.AbstractListModelMixin):
    pass


class StringListModel(StringListModelMixin, QtCore.QStringListModel):
    def __repr__(self):
        return f"{type(self).__name__}: ({self.rowCount()})"

    @classmethod
    def supports(cls, typ):
        match typ:
            case (str(), *_):
                return True
            case _:
                return False
