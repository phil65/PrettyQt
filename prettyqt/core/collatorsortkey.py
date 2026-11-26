from prettyqt.qt import QtCore


class CollatorSortKey(QtCore.QCollatorSortKey):
    """Can be used to speed up string collation."""
