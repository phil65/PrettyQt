from __future__ import annotations

from prettyqt import quick
from prettyqt.qt import QtQuick


class QuickAsyncImageProvider(
    quick.QuickImageProviderMixin, QtQuick.QQuickAsyncImageProvider
):
    pass
