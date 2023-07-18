from __future__ import annotations

from prettyqt.qt import QtCore


class SignalBlocker(QtCore.QSignalBlocker):
    """Exception-safe wrapper around QObject.blockSignals()."""
