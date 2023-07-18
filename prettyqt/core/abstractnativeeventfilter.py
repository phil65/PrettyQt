from __future__ import annotations

from prettyqt.qt import QtCore


class AbstractNativeEventFilter(QtCore.QAbstractNativeEventFilter):
    """Interface for receiving native events, such as MSG or XCB event structs."""

    def install(self):
        # theres also QCoreApplication::installNativeEventFilter. Not sure abt difference
        QtCore.QAbstractEventDispatcher.instance().installNativeEventFilter(self)
