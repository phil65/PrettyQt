from typing import TYPE_CHECKING

from prettyqt import qml
from prettyqt.qt import QtQuick


if TYPE_CHECKING:
    _QuickImageProviderBase = QtQuick.QQuickImageProvider
else:
    _QuickImageProviderBase = object


class QuickImageProviderMixin(qml.QmlImageProviderBaseMixin, _QuickImageProviderBase):
    pass


class QuickImageProvider(QuickImageProviderMixin, QtQuick.QQuickImageProvider):
    """Interface for supporting pixmaps and threaded image requests in QML."""
