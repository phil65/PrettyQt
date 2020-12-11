from qtpy import QtCore

from prettyqt import core


QtCore.QStringListModel.__bases__ = (core.AbstractListModel,)


class StringListModel(QtCore.QStringListModel):
    def serialize_fields(self):
        return dict(
            string_list=self.stringList(),
        )
