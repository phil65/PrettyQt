from prettyqt.qt import QtCore


class ModelIndex(QtCore.QModelIndex):
    """Used to locate data in a data model."""

    def __getitem__(self, flag: int):
        return self.data(flag)
