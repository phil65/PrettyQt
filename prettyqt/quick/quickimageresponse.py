from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


class QuickImageResponse(core.ObjectMixin, QtQuick.QQuickImageResponse):
    """Interface for asynchronous image loading in QQuickAsyncImageProvider."""


if __name__ == "__main__":
    item = QuickImageResponse()
