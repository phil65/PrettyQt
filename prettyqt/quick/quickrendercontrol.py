from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


class QuickRenderControl(core.ObjectMixin, QtQuick.QQuickRenderControl):
    pass


if __name__ == "__main__":
    item = QuickRenderControl()
