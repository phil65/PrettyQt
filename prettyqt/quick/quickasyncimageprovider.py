from prettyqt import quick
from prettyqt.qt import QtQuick


class QuickAsyncImageProvider(
    quick.QuickImageProviderMixin, QtQuick.QQuickAsyncImageProvider
):
    """Interface for asynchronous control of QML image requests."""
