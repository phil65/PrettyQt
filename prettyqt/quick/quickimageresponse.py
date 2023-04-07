from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


class QuickImageResponse(core.ObjectMixin, QtQuick.QQuickImageResponse):
    pass


if __name__ == "__main__":
    item = QuickImageResponse()
