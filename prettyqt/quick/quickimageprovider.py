from __future__ import annotations

from prettyqt import qml
from prettyqt.qt import QtQuick


class QuickImageProviderMixin(qml.QmlImageProviderBaseMixin):
    pass


class QuickImageProvider(QuickImageProviderMixin, QtQuick.QQuickImageProvider):
    """Interface for supporting pixmaps and threaded image requests in QML."""
