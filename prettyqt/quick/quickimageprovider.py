from __future__ import annotations

from prettyqt import qml
from prettyqt.qt import QtQuick


QtQuick.QQuickImageProvider.__bases__ = (qml.QmlImageProviderBase,)


class QuickImageProvider(QtQuick.QQuickImageProvider):
    pass
