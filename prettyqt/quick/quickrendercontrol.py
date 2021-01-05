from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


QtQuick.QQuickRenderControl.__bases__ = (core.Object,)


class QuickRenderControl(QtQuick.QQuickRenderControl):
    pass


if __name__ == "__main__":
    item = QuickRenderControl()
