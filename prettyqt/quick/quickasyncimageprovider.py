from __future__ import annotations

from prettyqt import quick
from prettyqt.qt import QtQuick


QtQuick.QQuickAsyncImageProvider.__bases__ = (quick.QuickImageProvider,)


class QuickAsyncImageProvider(QtQuick.QQuickAsyncImageProvider):
    pass
