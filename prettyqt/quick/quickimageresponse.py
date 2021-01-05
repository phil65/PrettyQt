from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


QtQuick.QQuickImageResponse.__bases__ = (core.Object,)


class QuickImageResponse(QtQuick.QQuickImageResponse):
    pass


if __name__ == "__main__":
    item = QuickImageResponse()
