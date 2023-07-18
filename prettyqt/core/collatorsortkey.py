from __future__ import annotations

from prettyqt.qt import QtCore


class CollatorSortKey(QtCore.QCollatorSortKey):
    """Can be used to speed up string collation."""
