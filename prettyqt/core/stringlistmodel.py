from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


class StringListModelMixin(core.AbstractListModelMixin):
    def serialize_fields(self):
        return dict(
            string_list=self.stringList(),
        )


class StringListModel(StringListModelMixin, QtCore.QStringListModel):
    pass
