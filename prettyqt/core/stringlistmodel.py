from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtCore


QtCore.QStringListModel.__bases__ = (core.AbstractListModel,)


class StringListModel(QtCore.QStringListModel):
    def serialize_fields(self):
        return dict(
            string_list=self.stringList(),
        )
