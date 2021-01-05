from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


QtQuick.QQuickTextDocument.__bases__ = (core.Object,)


class QuickTextDocument(QtQuick.QQuickTextDocument):
    pass


if __name__ == "__main__":
    item = QtQuick.QQuickItem()
    doc = QuickTextDocument(item)
