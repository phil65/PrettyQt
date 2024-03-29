from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQuick


class QuickTextDocument(core.ObjectMixin, QtQuick.QQuickTextDocument):
    """Access to the QTextDocument of QQuickTextEdit."""


if __name__ == "__main__":
    item = QtQuick.QQuickItem()
    doc = QuickTextDocument(item)
